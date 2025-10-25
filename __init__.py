import random
from aqt import mw
from aqt.qt import QAction, qconnect, QDialog, QVBoxLayout, QComboBox, QSpinBox, QPushButton, QLabel, QKeySequence
from aqt.utils import showInfo
from anki.notes import Note

def pick_random_words():
    # Custom dialog
    dialog = QDialog(mw)
    dialog.setWindowTitle("Pick Random Words")

    layout = QVBoxLayout()
    dialog.setLayout(layout)

    # Deck selection
    layout.addWidget(QLabel("Select deck:"))
    deck_combo = QComboBox()
    decks = mw.col.decks.all_names_and_ids()
    deck_names = [d.name for d in decks]
    deck_combo.addItems(deck_names)
    layout.addWidget(deck_combo)

    # Number of words
    layout.addWidget(QLabel("Number of words:"))
    num_spin = QSpinBox()
    num_spin.setRange(1, 100)
    num_spin.setValue(5)
    layout.addWidget(num_spin)

    # OK button
    ok_btn = QPushButton("Pick Words")
    layout.addWidget(ok_btn)

    def on_ok():
        deck_name = deck_combo.currentText()
        num = num_spin.value()

        deck_id = mw.col.decks.id(deck_name)
        card_ids = mw.col.decks.cids(deck_id)
        if not card_ids:
            showInfo("No cards found in that deck.")
            return

        random_ids = random.sample(card_ids, min(num, len(card_ids)))
        notes = [mw.col.get_card(cid).note() for cid in random_ids]
        fronts = [list(n.values())[0] for n in notes]

        message = "\n".join(fronts)
        showInfo(f"Random words from {deck_name}:\n\n{message}")
        dialog.close()

    ok_btn.clicked.connect(on_ok)
    dialog.exec()
    
# Menu action
action = QAction("Pick Random Words", mw)
action.setShortcut(QKeySequence("Shift+R"))
qconnect(action.triggered, pick_random_words)
mw.form.menuTools.addAction(action)