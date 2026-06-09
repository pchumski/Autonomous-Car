#!/usr/bin/env bash
# ============================================================
#  cleanup.sh — Autonomous-Car repo organiser
#  Uruchom z głównego folderu repozytorium:
#    bash cleanup.sh
# ============================================================

set -e  # zatrzymaj przy błędzie

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()    { echo -e "${GREEN}[✓]${NC} $1"; }
warn()    { echo -e "${YELLOW}[!]${NC} $1"; }
section() { echo -e "\n${YELLOW}=== $1 ===${NC}"; }

# ── Sprawdź czy jesteśmy w dobrym miejscu ──────────────────
if [ ! -f "README.md" ] || [ ! -d "Lane_detection" ]; then
    echo -e "${RED}[✗] Uruchom skrypt z głównego folderu repozytorium Autonomous-Car!${NC}"
    exit 1
fi

section "Tworzenie struktury old/"
mkdir -p old/model_metrics_duplicates
info "Foldery old/ gotowe"

# ── Helper: bezpieczne przenoszenie ────────────────────────
move() {
    local src="$1" dst="$2"
    if [ -e "$src" ]; then
        mv "$src" "$dst"
        info "Przeniesiono: $src → $dst"
    else
        warn "Już przeniesione lub nie istnieje: $src"
    fi
}

# ── 1. Notatniki Keras (nauka, nie projekt) ────────────────
section "1. Keras — notatniki do nauki"
move "Keras" "old/Keras"

# ── 2. Self learning — tutoriale OpenCV ───────────────────
section "2. Self learning — materiały szkoleniowe"
move "self learning" "old/self_learning"

# ── 3. Transit project — stary projekt przejściowy ────────
section "3. Transit project — stary projekt"
move "transit project" "old/transit_project"

# ── 4. Stara prezentacja ──────────────────────────────────
section "4. Stara prezentacja"
move "presentation/Autonomous_car_old.pdf" "old/Autonomous_car_old.pdf"

# ── 5. Tutoriale YOLOv5 ───────────────────────────────────
section "5. Yolov5/Computer/tutorial — pliki tutorialowe"
move "Yolov5/Computer/tutorial" "old/yolov5_tutorial"

# ── 6. Eksperymentalne skrypty Lane_detection/test ────────
section "6. Lane_detection/test — skrypty testowe"
move "Lane_detection/test" "old/lane_detection_test"

# ── 7. Screenshoty w Gamepad/Own gamepad ──────────────────
section "7. Screenshoty gamepad"
for f in "Gamepad/Own gamepad"/screen*.jpg; do
    [ -e "$f" ] && move "$f" "old/"
done

# ── 8. Duplikaty z wskazniki_jakosci_modelu ───────────────
section "8. Duplikaty plików (— kopia)"
find "Yolov5/Jetracer/wskazniki_jakosci_modelu/" -name "*kopia*" 2>/dev/null | while read -r f; do
    move "$f" "old/model_metrics_duplicates/"
done

# ── Podsumowanie ──────────────────────────────────────────
section "Gotowe!"
echo ""
echo "Zawartość old/:"
find old/ -maxdepth 2 | sort
echo ""
echo -e "${GREEN}Możesz teraz commitować zmiany:${NC}"
echo "  git add -A"
echo "  git commit -m \"chore: move legacy/experimental files to old/\""
echo "  git push"
