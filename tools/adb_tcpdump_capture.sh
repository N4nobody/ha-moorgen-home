#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./tools/adb_tcpdump_capture.sh -h 192.168.1.246 [-p 9000] [-i any] [-o ./capture.pcap] [--no-su] [--tcpdump-bin /data/local/tmp/tcpdump]

HOST="192.168.1.246"
PORT="9000"
IFACE="any"
LOCAL_OUT="resources/"
USE_SU="1"
TCPDUMP_BIN="tcpdump"

usage() {
  cat <<EOF
Usage: $0 -h <host_ip> [options]

Required:
  -h, --host              Target host IP (e.g. Moorgen gateway)

Options:
  -p, --port              TCP port (default: 9000)
  -i, --iface             Capture interface on Android (default: any)
  -o, --out               Local output pcap path (default: ./moorgen_<timestamp>.pcap)
      --no-su             Do not use su -c when running tcpdump
      --tcpdump-bin       tcpdump path on device (default: tcpdump)
      --help              Show this help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--host)
      HOST="$2"; shift 2;;
    -p|--port)
      PORT="$2"; shift 2;;
    -i|--iface)
      IFACE="$2"; shift 2;;
    -o|--out)
      LOCAL_OUT="$2"; shift 2;;
    --no-su)
      USE_SU="0"; shift;;
    --tcpdump-bin)
      TCPDUMP_BIN="$2"; shift 2;;
    --help)
      usage; exit 0;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1;;
  esac
done

if [[ -z "$HOST" ]]; then
  echo "Error: --host is required" >&2
  usage
  exit 1
fi

if ! command -v adb >/dev/null 2>&1; then
  echo "Error: adb not found in PATH" >&2
  exit 1
fi

adb wait-for-device >/dev/null

TS="$(date +%Y%m%d_%H%M%S)"
REMOTE_FILE="/sdcard/moorgen_${TS}.pcap"
if [[ -z "$LOCAL_OUT" ]]; then
  LOCAL_OUT="./moorgen_${TS}.pcap"
fi

FILTER="host ${HOST} and tcp port ${PORT}"
BASE_CMD="${TCPDUMP_BIN} -i ${IFACE} ${FILTER} -s 0 -w ${REMOTE_FILE}"
if [[ "$USE_SU" == "1" ]]; then
  REMOTE_CMD="su -c '${BASE_CMD}'"
else
  REMOTE_CMD="${BASE_CMD}"
fi

CAP_PID=""
STOPPED="0"
IN_CLEANUP="0"

stop_and_collect() {
  if [[ "$STOPPED" == "1" || "$IN_CLEANUP" == "1" ]]; then
    return
  fi

  IN_CLEANUP="1"
  STOPPED="1"

  # Prevent re-entrant traps when user presses Ctrl+C again during cleanup.
  trap '' INT TERM
  trap - EXIT

  echo
  echo "[1/3] Stopping tcpdump..."

  # 1) Ask remote tcpdump to stop first.
  if [[ "$USE_SU" == "1" ]]; then
    adb shell "su -c 'pkill -INT -f \"${TCPDUMP_BIN}\" || true'" >/dev/null 2>&1 || true
  else
    adb shell "pkill -INT -f \"${TCPDUMP_BIN}\" || true" >/dev/null 2>&1 || true
  fi

  # 2) Stop local adb shell process if still alive.
  if [[ -n "$CAP_PID" ]] && kill -0 "$CAP_PID" 2>/dev/null; then
    kill -TERM "$CAP_PID" 2>/dev/null || true
    for _ in {1..20}; do
      if ! kill -0 "$CAP_PID" 2>/dev/null; then
        break
      fi
      sleep 0.1
    done
    if kill -0 "$CAP_PID" 2>/dev/null; then
      kill -KILL "$CAP_PID" 2>/dev/null || true
    fi
    wait "$CAP_PID" 2>/dev/null || true
  fi

  echo "[2/3] Pulling pcap to local: ${LOCAL_OUT}"
  adb pull "$REMOTE_FILE" "$LOCAL_OUT" || true

  echo "[3/3] Deleting remote pcap: ${REMOTE_FILE}"
  if [[ "$USE_SU" == "1" ]]; then
    adb shell "su -c 'rm -f ${REMOTE_FILE}'" >/dev/null || true
  else
    adb shell "rm -f ${REMOTE_FILE}" >/dev/null || true
  fi

  echo "Done: ${LOCAL_OUT}"
}

trap 'stop_and_collect; exit 130' INT
trap '[[ "$STOPPED" == "0" ]] && stop_and_collect' EXIT

echo "Starting capture on device..."
echo "  Host : ${HOST}"
echo "  Port : ${PORT}"
echo "  Iface: ${IFACE}"
echo "  Remote file: ${REMOTE_FILE}"
echo "Press Ctrl+C to stop and collect."

adb shell "$REMOTE_CMD" &
CAP_PID=$!
wait "$CAP_PID"
