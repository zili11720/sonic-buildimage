#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: NVIDIA CORPORATION & AFFILIATES
# Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Gate process: runs phcsync.sh as a child and pauses / resumes when warm reboot is detected.
# Uses swsscommon RestartWaiter (event-driven, no DB polling).
#

import os
import signal
import sys
import syslog
import subprocess

try:
    from swsscommon.swsscommon import RestartWaiter
except ImportError:
    syslog.syslog(syslog.LOG_ERR, "phcsync_warm_reboot_gate: swsscommon not available")
    sys.exit(1)

PHCSYNC_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phcsync.sh")
WARM_BOOT_STARTED_TIMEOUT_SEC = 86400  # 24h
WARM_BOOT_DONE_TIMEOUT_SEC = 180


def log(msg, level=syslog.LOG_INFO):
    syslog.syslog(level, msg)


def main():
    syslog.openlog("phcsync-warm-reboot-gate", syslog.LOG_PID)

    if not os.path.isfile(PHCSYNC_SCRIPT) or not os.access(PHCSYNC_SCRIPT, os.X_OK):
        log("phcsync script not found or not executable: %s" % PHCSYNC_SCRIPT, syslog.LOG_ERR)
        return 1

    child_proc = None

    def shutdown(signum, frame):
        if child_proc and child_proc.pid is not None:
            try:
                child_proc.terminate()
                child_proc.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    child_proc.kill()
                except ProcessLookupError:
                    pass
        sys.exit(128 + (signum if signum in (signal.SIGINT, signal.SIGTERM) else 0))

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    try:
        child_proc = subprocess.Popen(
            [PHCSYNC_SCRIPT],
            preexec_fn=os.setpgrp if hasattr(os, "setpgrp") else None,
        )
    except Exception as e:
        log("Failed to start %s: %s" % (PHCSYNC_SCRIPT, e), syslog.LOG_ERR)
        return 1

    log("Started phcsync (pid %d), listening for warm reboot" % child_proc.pid)

    while True:
        if not RestartWaiter.waitWarmBootStarted(maxWaitSec=WARM_BOOT_STARTED_TIMEOUT_SEC):
            log("waitWarmBootStarted timed out, continuing loop")
            continue

        pid = child_proc.pid
        if pid is None:
            break
        try:
            _pid, _ = os.waitpid(pid, os.WNOHANG)
            if _pid != 0:
                log("phcsync exited (pid=%d), gate exiting" % pid, syslog.LOG_WARNING)
                return 2
        except ChildProcessError:
            break

        log("Warm reboot started, pausing phcsync")
        try:
            os.kill(pid, signal.SIGSTOP)
        except ProcessLookupError:
            log("phcsync process gone, exiting", syslog.LOG_WARNING)
            return 2

        if not RestartWaiter.waitWarmBootDone(maxWaitSec=WARM_BOOT_DONE_TIMEOUT_SEC):
            log("waitWarmBootDone timed out, resuming phcsync anyway", syslog.LOG_WARNING)

        try:
            os.kill(pid, signal.SIGCONT)
        except ProcessLookupError:
            log("phcsync process gone while paused, exiting", syslog.LOG_WARNING)
            return 2
        log("Warm reboot done, resumed phcsync")

    return 2


if __name__ == "__main__":
    sys.exit(main())
