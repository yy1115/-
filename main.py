import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox, QDialog,
                             QRadioButton, QLineEdit, QScrollArea, QFrame, QTabWidget,
                             QFormLayout, QComboBox, QSizePolicy, QSpacerItem,
                             QGraphicsDropShadowEffect) # Import for shadows
from PyQt5.QtGui import QTextCursor, QColor, QIcon, QFont, QPalette
from PyQt5.QtCore import Qt, pyqtSignal

# --- Mock implementations for testing ---
class MockAudio2Text:
    def transcribe(self, path):
        print(f"Mock Transcribing: {path}")
        # Simulate a bit of delay
        for _ in range(10000000): pass
        return f"Mock transcribed text from {path.split('/')[-1]} about a sunny day at the beach with laughter and waves."

class config:
    prompt2 = "Mock prompt: Weave these memories into a cohesive and evocative story."

def get_result(prompt, combined_text):
    print(f"Mock get_result with prompt: {prompt}")
    print(f"Mock processing combined text:\n{combined_text}")
    # Simulate a bit of delay
    for _ in range(10000000): pass
    return (f"This is the AI woven narrative based on the provided memories:\n\n"
            f"{combined_text}\n\n"
            f"The story unfolds, revealing shared joys and unique perspectives, painting a vivid picture of the summer beach trip. "
            f"Laughter echoed with the crashing waves, and the setting sun cast long shadows on the golden sand, "
            f"etching these moments into a collective, cherished remembrance.")
# --- End Mock implementations ---

Audio2Text = MockAudio2Text

# --- Global Styles and Fonts ---
APP_FONT = QFont("Segoe UI", 10) # A common modern font
BASE_TEXT_COLOR = "#334155"     # Slate 700
LIGHT_TEXT_COLOR = "#64748b"    # Slate 500
PRIMARY_COLOR = "#4f46e5"       # Indigo 600
PRIMARY_HOVER_COLOR = "#4338ca"  # Indigo 700
PRIMARY_LIGHT_BG = "#e0e7ff"    # Indigo 100
PRIMARY_LIGHT_TEXT = "#3730a3"  # Indigo 800
SECONDARY_BUTTON_BG = "#e2e8f0" # Slate 200
SECONDARY_BUTTON_TEXT = "#334155" # Slate 700
SECONDARY_BUTTON_HOVER_BG = "#cbd5e1" # Slate 300
BORDER_COLOR = "#cbd5e1"        # Slate 300
BACKGROUND_COLOR_LIGHT = "#f8fafc" # Slate 50
BACKGROUND_COLOR_MAIN = "#f1f5f9" # Slate 100
WHITE_COLOR = "#ffffff"
SUCCESS_COLOR = "#10b981"       # Green 500
SUCCESS_HOVER_COLOR = "#059669"  # Green 600
ERROR_COLOR = "#ef4444"         # Red 500

class MemoryInputDialog(QDialog):
    memory_submitted = pyqtSignal(str, str, str, str)

    def __init__(self, memory_type="Text", parent=None):
        super().__init__(parent)
        self.memory_type = memory_type
        self.text_result = ""
        self.file_path = ""
        self.initUI()
        self.apply_shadow()

    def apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

    def initUI(self):
        self.setWindowTitle(f"Add {self.memory_type} Memory")
        self.setMinimumWidth(480) # Increased width
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {BACKGROUND_COLOR_LIGHT};
                border-radius: 8px; /* Rounded corners for the dialog itself */
            }}
            QLabel {{
                font-size: 10pt;
                color: {BASE_TEXT_COLOR};
                margin-bottom: 4px;
            }}
            QLineEdit, QTextEdit, QComboBox {{
                border: 1px solid {BORDER_COLOR};
                border-radius: 6px;
                padding: 8px 10px; /* Increased padding */
                background-color: {WHITE_COLOR};
                font-size: 10pt;
                color: {BASE_TEXT_COLOR};
            }}
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
                border: 1px solid {PRIMARY_COLOR};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: url(down_arrow.png); /* Placeholder: Needs an actual icon */
                width: 12px;
                height: 12px;
                margin-right: 5px;
            }}
            QPushButton {{
                border-radius: 6px;
                padding: 10px 15px; /* Increased padding */
                font-size: 10pt;
                font-weight: 500; /* Medium weight */
            }}
            QPushButton#submitButton {{
                background-color: {PRIMARY_COLOR};
                color: {WHITE_COLOR};
            }}
            QPushButton#submitButton:hover {{ background-color: {PRIMARY_HOVER_COLOR}; }}
            QPushButton#submitButton:pressed {{ background-color: {PRIMARY_COLOR}; }}

            QPushButton#cancelButton {{
                background-color: {SECONDARY_BUTTON_BG};
                color: {SECONDARY_BUTTON_TEXT};
            }}
            QPushButton#cancelButton:hover {{ background-color: {SECONDARY_BUTTON_HOVER_BG}; }}
            QPushButton#cancelButton:pressed {{ background-color: {SECONDARY_BUTTON_BG}; }}

            QPushButton#browseButton {{
                background-color: {PRIMARY_LIGHT_BG};
                color: {PRIMARY_LIGHT_TEXT};
                font-weight: normal;
            }}
             QPushButton#browseButton:hover {{ background-color: #c7d2fe; }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20) # More padding inside dialog
        layout.setSpacing(15) # Spacing between elements

        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        form_layout.setLabelAlignment(Qt.AlignRight) # Align labels to the right

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("E.g., Jane Doe")
        form_layout.addRow("Your Name:", self.name_input)

        if self.memory_type == "Text":
            self.text_input_area = QTextEdit()
            self.text_input_area.setPlaceholderText("Describe your memory...")
            self.text_input_area.setMinimumHeight(100)
            form_layout.addRow("Memory Content:", self.text_input_area)
        elif self.memory_type == "Audio":
            self.audio_path_display = QLineEdit()
            self.audio_path_display.setReadOnly(True)
            self.audio_path_display.setPlaceholderText("No audio file selected")
            self.browse_btn = QPushButton("🎤 Select Audio File...", objectName="browseButton")
            self.browse_btn.clicked.connect(self.select_audio_file)
            audio_layout = QHBoxLayout()
            audio_layout.addWidget(self.audio_path_display)
            audio_layout.addWidget(self.browse_btn)
            form_layout.addRow("Audio File:", audio_layout)

        self.emotion_combo = QComboBox()
        self.emotion_combo.addItems(["Nostalgia", "Excitement", "Peace", "Joy", "Moved", "Awe", "Humor", "Other"])
        form_layout.addRow("Emotion Tag:", self.emotion_combo)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.cancel_btn = QPushButton("Cancel", objectName="cancelButton")
        self.cancel_btn.clicked.connect(self.reject)
        self.submit_btn = QPushButton(f"Submit Memory", objectName="submitButton")
        self.submit_btn.clicked.connect(self.validate_and_accept)

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.submit_btn)
        layout.addLayout(button_layout)

    def select_audio_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.ogg *.m4a)")
        if path:
            self.file_path = path
            self.audio_path_display.setText(path.split('/')[-1]) # Show only filename

    def validate_and_accept(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter your name.")
            return

        emotion = self.emotion_combo.currentText()
        content_for_card_display = "" # This is what will be shown on the card initially
        transcribed_text_for_processing = "" # This is what goes to the AI

        try:
            if self.memory_type == "Text":
                text_content = self.text_input_area.toPlainText().strip()
                if not text_content:
                    QMessageBox.warning(self, "Input Error", "Memory content cannot be empty.")
                    return
                content_for_card_display = text_content
                transcribed_text_for_processing = text_content
            elif self.memory_type == "Audio":
                if not self.file_path:
                    QMessageBox.warning(self, "Input Error", "Please select an audio file.")
                    return

                loading_dialog = QMessageBox(self)
                loading_dialog.setWindowTitle("Transcribing...")
                loading_dialog.setText("Processing audio file, please wait. This might take a moment.")
                loading_dialog.setIcon(QMessageBox.Information)
                loading_dialog.setStandardButtons(QMessageBox.NoButton) # No buttons
                loading_dialog.show()
                QApplication.processEvents()

                a2t = Audio2Text()
                transcribed_text_for_processing = a2t.transcribe(self.file_path)
                loading_dialog.close()

                if not transcribed_text_for_processing:
                    QMessageBox.warning(self, "Processing Error", "Could not transcribe audio or audio is silent.")
                    return
                # For the card, we want to show both the file and the transcription
                content_for_card_display = (f"🗣️ Audio: {self.file_path.split('/')[-1]}\n\n"
                                            f"📜 Transcription:\n{transcribed_text_for_processing[:150]}...") # Show a snippet

            # Emit the transcribed text for AI, but potentially different content for card display
            self.memory_submitted.emit(name, self.memory_type, transcribed_text_for_processing, emotion)
            self.accept()

        except Exception as e:
            if 'loading_dialog' in locals() and loading_dialog.isVisible():
                loading_dialog.close()
            QMessageBox.critical(self, "Processing Error", f"An error occurred: {str(e)}")
            self.reject()


class MemoryCard(QFrame):
    def __init__(self, name, memory_type, content_for_display, emotion, timestamp="Just now", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame) # Remove default frame, styling via QSS
        self.setObjectName("MemoryCard")
        self.setStyleSheet(f"""
            #MemoryCard {{
                background-color: {WHITE_COLOR};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px; /* Softer corners */
                padding: 15px;     /* More padding */
                margin-bottom: 12px;
            }}
            QLabel#nameLabel {{
                font-weight: bold;
                font-size: 11pt;
                color: {BASE_TEXT_COLOR};
            }}
            QLabel#timestampLabel {{
                font-size: 8pt;
                color: {LIGHT_TEXT_COLOR};
            }}
            QLabel#emotionLabel {{
                font-size: 9pt;
                color: {PRIMARY_LIGHT_TEXT}; /* Indigo text */
                background-color: {PRIMARY_LIGHT_BG}; /* Light indigo bg */
                padding: 4px 8px; /* More padding */
                border-radius: 12px; /* Pill shape */
            }}
            QTextEdit#contentArea {{
                border: none;
                background-color: transparent;
                font-size: 10pt;
                color: {BASE_TEXT_COLOR};
                padding: 0;
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10) # Spacing between elements in card

        header_layout = QHBoxLayout()
        name_label = QLabel(name, objectName="nameLabel")
        timestamp_label = QLabel(timestamp, objectName="timestampLabel")
        header_layout.addWidget(name_label)
        header_layout.addStretch()
        header_layout.addWidget(timestamp_label)
        main_layout.addLayout(header_layout)

        content_display = QTextEdit(objectName="contentArea")
        # The `content_for_display` is now passed directly
        content_display.setPlainText(content_for_display)
        content_display.setReadOnly(True)
        # Adjust height based on content, or set a fixed reasonable height
        doc_height = content_display.document().size().height()
        content_display.setFixedHeight(min(max(int(doc_height) + 5, 60), 150)) # Dynamic height with min/max

        main_layout.addWidget(content_display)

        footer_layout = QHBoxLayout()
        emotion_text = f"😊 {emotion}" # Adding an emoji
        emotion_label = QLabel(emotion_text, objectName="emotionLabel")
        footer_layout.addWidget(emotion_label)
        footer_layout.addStretch()
        main_layout.addLayout(footer_layout)

        # Apply shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 40)) # Softer shadow
        self.setGraphicsEffect(shadow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memories_data = []
        self.initUI()
        self.update_status_labels() # Initial update

    def initUI(self):
        self.setWindowTitle("Collective Memory Weaver")
        self.setGeometry(50, 50, 950, 750) # Slightly larger window
        self.setFont(APP_FONT) # Apply global font
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {BACKGROUND_COLOR_MAIN}; }}
            QTabWidget::pane {{
                border: none; /* Remove border around tab content area */
                padding: 0px;
            }}
            QTabBar::tab {{
                background: transparent; /* Make inactive tabs blend with pane */
                color: {LIGHT_TEXT_COLOR};
                border: none;
                border-bottom: 2px solid transparent; /* Underline for active tab */
                padding: 12px 20px; /* More padding */
                margin-right: 5px;
                font-size: 11pt; /* Larger tab font */
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background: transparent;
                color: {PRIMARY_COLOR}; /* Indigo */
                border-bottom: 2px solid {PRIMARY_COLOR};
            }}
            QTabBar::tab:hover {{
                background: transparent;
                color: {PRIMARY_COLOR};
                border-bottom: 2px solid #a5b4fc; /* Lighter indigo for hover underline */
            }}
            QPushButton#actionButton {{ /* For Generate button */
                background-color: {SUCCESS_COLOR};
                color: white;
                border-radius: 6px;
                padding: 12px 20px; /* More padding */
                font-size: 11pt;
                font-weight: bold;
            }}
            QPushButton#actionButton:hover {{ background-color: {SUCCESS_HOVER_COLOR}; }}
            QPushButton#actionButton:pressed {{ background-color: {SUCCESS_COLOR}; }}

            QLabel#headerTitle {{
                font-size: 20pt; font-weight: bold; color: {WHITE_COLOR};
                padding-bottom: 5px; /* Spacing below title */
            }}
            QLabel#headerSubtitle {{ font-size: 10pt; color: #e0e7ff; /* Lighter for subtitles */ }}
            QLabel#statusBadge {{
                font-size: 9pt; font-weight: 500;
                padding: 5px 10px; border-radius: 12px; /* Pill shape */
            }}
            QScrollArea {{ border: none; background-color: transparent; }}
            QWidget#scrollAreaWidgetContents {{ background-color: transparent; }}
            QTextEdit#resultsDisplay {{ /* Styling the results text edit */
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
                padding: 15px;
                background-color: {WHITE_COLOR};
                font-size: 10pt;
                color: {BASE_TEXT_COLOR};
            }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0) # No spacing between header, tabs, footer

        # --- Header ---
        header_widget = QWidget(objectName="appHeader")
        header_widget.setStyleSheet(f"#appHeader {{ background-color: {PRIMARY_COLOR}; padding: 20px 25px; }}")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(5)

        title_label = QLabel("Summer Beach Trip (Demo)", objectName="headerTitle")
        header_layout.addWidget(title_label)

        info_layout = QHBoxLayout()
        self.participants_label = QLabel("Contributors: 0", objectName="headerSubtitle")
        self.status_label = QLabel("Status: Idle", objectName="statusBadge") # Use specific name
        info_layout.addWidget(self.participants_label)
        info_layout.addStretch()
        info_layout.addWidget(self.status_label)
        header_layout.addLayout(info_layout)
        main_layout.addWidget(header_widget)

        # --- Tab Widget ---
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(20, 20, 20, 20) # Padding for tab content area
        main_layout.addWidget(self.tabs)

        # --- Tab 1: Contribute Memory ---
        self.contribute_tab = QWidget()
        self.tabs.addTab(self.contribute_tab, "📝 Contribute Memory")
        contribute_layout = QVBoxLayout(self.contribute_tab)
        contribute_layout.setContentsMargins(0, 15, 0, 0) # Top margin for content
        contribute_layout.setSpacing(15)

        add_memory_group = QWidget()
        add_memory_layout = QHBoxLayout(add_memory_group)
        add_memory_layout.setContentsMargins(0,0,0,0)

        add_memory_label = QLabel("Add New Memory:")
        add_memory_label.setStyleSheet(f"font-size: 13pt; font-weight: bold; color: {BASE_TEXT_COLOR};")
        add_memory_layout.addWidget(add_memory_label)
        add_memory_layout.addStretch(1)

        self.add_text_btn = QPushButton("✍️ Text")
        self.add_voice_btn = QPushButton("🎤 Voice")
        # self.add_image_btn = QPushButton("🖼️ Image") # Placeholder
        # self.add_image_btn.setEnabled(False)

        button_style = f"""
            QPushButton {{
                background-color: {PRIMARY_LIGHT_BG}; color: {PRIMARY_LIGHT_TEXT};
                border: 1px solid #c7d2fe; border-radius: 6px;
                padding: 10px 18px; font-size: 10pt; font-weight: 500;
            }}
            QPushButton:hover {{ background-color: #c7d2fe; }}
            QPushButton:pressed {{ background-color: {PRIMARY_LIGHT_BG}; }}
        """
        self.add_text_btn.setStyleSheet(button_style)
        self.add_voice_btn.setStyleSheet(button_style)
        # self.add_image_btn.setStyleSheet(button_style)

        self.add_text_btn.clicked.connect(lambda: self.open_memory_dialog("Text"))
        self.add_voice_btn.clicked.connect(lambda: self.open_memory_dialog("Audio"))

        add_memory_layout.addWidget(self.add_text_btn)
        add_memory_layout.addWidget(self.add_voice_btn)
        # add_memory_layout.addWidget(self.add_image_btn)
        contribute_layout.addWidget(add_memory_group)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget(objectName="scrollAreaWidgetContents")
        self.memories_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.memories_layout.setAlignment(Qt.AlignTop)
        self.memories_layout.setContentsMargins(0,0,5,0) # Small right margin for scrollbar
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        contribute_layout.addWidget(self.scroll_area)

        # --- Tab 2: Woven Results ---
        self.woven_tab = QWidget()
        self.tabs.addTab(self.woven_tab, "✨ Woven Results")
        woven_layout = QVBoxLayout(self.woven_tab)
        woven_layout.setContentsMargins(0, 15, 0, 0)

        self.results_display_label = QLabel("Collective Memory Narrative:")
        self.results_display_label.setStyleSheet(f"font-size: 13pt; font-weight: bold; color: {BASE_TEXT_COLOR}; margin-bottom: 10px;")
        woven_layout.addWidget(self.results_display_label)

        self.result_display_text = QTextEdit(objectName="resultsDisplay")
        self.result_display_text.setReadOnly(True)
        woven_layout.addWidget(self.result_display_text, 1)

        # --- Tab 3: Interactive Discussion (Placeholder) ---
        self.interactions_tab = QWidget()
        self.tabs.addTab(self.interactions_tab, "🗣️ Discussion")
        interactions_layout = QVBoxLayout(self.interactions_tab)
        interactions_layout.setContentsMargins(0, 15, 0, 0)
        placeholder_label = QLabel("Interactive discussion features would be implemented here.")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setStyleSheet(f"font-size: 11pt; color: {LIGHT_TEXT_COLOR};")
        interactions_layout.addWidget(placeholder_label)

        # --- Footer ---
        footer_widget = QWidget(objectName="appFooter")
        footer_widget.setStyleSheet(f"#appFooter {{ background-color: {WHITE_COLOR}; padding: 12px 25px; border-top: 1px solid {BORDER_COLOR}; }}")
        footer_layout = QHBoxLayout(footer_widget)

        self.generation_status_label = QLabel("Collected Memories: 0")
        self.generation_status_label.setStyleSheet(f"font-size: 10pt; color: {BASE_TEXT_COLOR};")
        footer_layout.addWidget(self.generation_status_label)
        footer_layout.addStretch()

        self.generate_btn = QPushButton("🚀 Generate Collective Memory", objectName="actionButton")
        self.generate_btn.clicked.connect(self.process_memories)
        footer_layout.addWidget(self.generate_btn)
        main_layout.addWidget(footer_widget)

    def open_memory_dialog(self, memory_type):
        dialog = MemoryInputDialog(memory_type, self)
        # Make dialog semi-transparent during drag for a modern effect (optional)
        # dialog.setWindowOpacity(0.95)
        dialog.memory_submitted.connect(self.add_memory_card_data) # Connect to new slot
        dialog.exec_()

    def add_memory_card_data(self, name, memory_type, transcribed_text_for_processing, emotion):
        # Prepare content for card display
        # For text, it's the text itself. For audio, it's a mix.
        content_for_card = ""
        if memory_type == "Text":
            content_for_card = transcribed_text_for_processing
        elif memory_type == "Audio":
             # Find the original file path - tricky if not passed directly.
             # For simplicity, we'll just use the transcription on the card as well if path isn't available.
             # A better way would be to pass the file_path also through the signal or store it temporarily.
             # For now, let's assume 'transcribed_text_for_processing' is sufficient for the card's detail.
            content_for_card = (f"🗣️ Audio Memory (Transcription):\n\n"
                                f"{transcribed_text_for_processing[:200]}"
                                f"{'...' if len(transcribed_text_for_processing) > 200 else ''}")


        self.memories_data.append({
            "name": name,
            "type": memory_type,
            "content_for_processing": transcribed_text_for_processing, # This goes to AI
            "content_for_card": content_for_card, # This is for the card display
            "emotion": emotion,
            "timestamp": "Just now" # Or use datetime
        })

        # Create and add card widget
        card = MemoryCard(name, memory_type, content_for_card, emotion, "Just now")
        self.memories_layout.insertWidget(0, card) # Insert at top for newest first
        self.update_status_labels()
        # Simple success message without modal for smoother flow
        self.statusBar().showMessage(f"{memory_type} memory from {name} added!", 3000)


    def update_status_labels(self):
        count = len(self.memories_data)
        unique_contributors = len(set(m['name'] for m in self.memories_data))
        self.participants_label.setText(f"Contributors: {unique_contributors}")
        self.generation_status_label.setText(f"Collected Memories: {count}")

        if count > 0:
             self.status_label.setText("Collecting...")
             self.status_label.setStyleSheet(f"color: {PRIMARY_LIGHT_TEXT}; background-color: {PRIMARY_LIGHT_BG}; padding: 5px 10px; border-radius: 12px;")
        else:
            self.status_label.setText("Idle")
            self.status_label.setStyleSheet(f"color: {LIGHT_TEXT_COLOR}; background-color: {SECONDARY_BUTTON_BG}; padding: 5px 10px; border-radius: 12px;")
        self.generate_btn.setEnabled(count > 0)


    def process_memories(self):
        if not self.memories_data:
            QMessageBox.warning(self, "No Memories", "Please add some memories before generating.")
            return

        self.result_display_text.clear()
        loading_msg = ("<p style='color:#64748b; font-size:11pt; text-align:center;'>"
                       "🚀 Weaving memories together... <br>This might take a moment.</p>")
        self.result_display_text.setHtml(loading_msg)
        self.tabs.setCurrentWidget(self.woven_tab)
        QApplication.processEvents()

        try:
            combined_input_texts = []
            for i, mem_data in enumerate(self.memories_data):
                combined_input_texts.append(f"{i+1}. {mem_data['name']} ({mem_data['emotion']}): {mem_data['content_for_processing']}")
            combined = "\n\n".join(combined_input_texts) # More spacing between entries

            self.result_display_text.clear()
            cursor = self.result_display_text.textCursor()

            # --- Contributed Memories Section ---
            fmt_heading = cursor.charFormat()
            fmt_heading.setFontPointSize(13)
            fmt_heading.setFontWeight(QFont.Bold)
            fmt_heading.setForeground(QColor(BASE_TEXT_COLOR))
            cursor.insertText("📝 Contributed Memories\n\n", fmt_heading)

            fmt_memory_item = cursor.charFormat()
            fmt_memory_item.setFontPointSize(10)
            fmt_memory_item.setForeground(QColor(LIGHT_TEXT_COLOR))

            for i, mem_data in enumerate(self.memories_data):
                item_text = (f"👤 {mem_data['name']} ({mem_data['emotion']}):\n"
                             f"{mem_data['content_for_processing']}\n\n")
                cursor.insertText(item_text, fmt_memory_item)

            # --- Woven Narrative Section ---
            cursor.insertText("\n✨ Woven Narrative\n\n", fmt_heading)

            ai_result = get_result(config.prompt2, combined)
            fmt_narrative = cursor.charFormat()
            fmt_narrative.setFontPointSize(11) # Slightly larger for narrative
            fmt_narrative.setForeground(QColor(BASE_TEXT_COLOR))
            fmt_narrative.setLineHeight(150, QFont.ProportionalHeight) # Line spacing
            cursor.insertText(ai_result, fmt_narrative)

            self.status_label.setText("Generated!")
            self.status_label.setStyleSheet(f"color: {WHITE_COLOR}; background-color: {SUCCESS_COLOR}; padding: 5px 10px; border-radius: 12px;")
            self.statusBar().showMessage("Collective memory generated successfully!", 5000)

        except Exception as e:
            self.result_display_text.setHtml(f"<p style='color:{ERROR_COLOR};'>Error during processing: {str(e)}</p>")
            QMessageBox.critical(self, "Processing Error", f"Failed to generate results: {str(e)}")
            self.status_label.setText("Error")
            self.status_label.setStyleSheet(f"color: {WHITE_COLOR}; background-color: {ERROR_COLOR}; padding: 5px 10px; border-radius: 12px;")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirm Exit', 'Are you sure you want to exit the Collective Memory Weaver?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle('Fusion') # Fusion can sometimes provide a cleaner base
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())