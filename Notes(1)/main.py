import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from tkinter import messagebox, filedialog
import os
from PySide6.QtGui import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import *
from qframelesswindow import *


write_icon = QIcon("resource/write.svg")
about_icon = QIcon("resources/write.svg")

# Stylesheet
style_sheet = f"""
        QMenuBar {{
            background-color: #323232;
        }}
        QMenuBar::item {{
            background-color: #323232;
            color: red;
        }}
        QMenuBar::item::selected {{
            background-color: #1b1b1b;
        }}
        QMenu {{
            background-color: rgb(49, 49, 49);
            color: red;
            border: 0px solid #000;
        }}
        QMenu::item::selected {{
            background-color: rgb(30, 30, 30);
        }}

    """

class TWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFont(QFont("DotNess", 16))
        self.setAcceptRichText(False)
        self.setStyleSheet("QTextEdit{background-color : #000000; color : white; border: 0;}")

    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)
        #menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)

        # NOTE: hide the shortcut key
        # menu.view.setItemDelegate(MenuItemDelegate())

        copy_action = Action(FIF.COPY, 'Copy')
        copy_action.triggered.connect(lambda : self.copy())

        # Create an action for cut
        cut_action = Action(FIF.CUT, 'Cut')
        cut_action.triggered.connect(lambda: self.cut())

        # Create an action for copy
        copy_action = Action(FIF.COPY, 'Copy')
        copy_action.triggered.connect(lambda: self.copy())

        # Create an action for paste
        paste_action = Action(FIF.PASTE, 'Paste')
        paste_action.triggered.connect(lambda: self.paste())

        # Create an action for undo
        undo_action = Action(FIF.CANCEL, 'Undo')
        undo_action.triggered.connect(lambda: self.undo())

        # Create an action for redo
        redo_action = Action(FIF.EMBED, 'Redo')
        redo_action.triggered.connect(lambda: self.redo())

        # Create an action for select all
        select_all_action = Action(FIF.EMBED, 'Select All')
        select_all_action.triggered.connect(lambda: self.selectAll())

        # add actions
        menu.addAction(copy_action)
        menu.addAction(cut_action)
        menu.actions()[0].setCheckable(True)
        menu.actions()[0].setChecked(True)

        # add sub menu
        #submenu = RoundMenu("Add to", self)
        #submenu.setIcon(FIF.ADD)
        #submenu.addActions([
        #    QAction('Video'),
        #    Action(FIF.MUSIC, 'Music'),
        #])
        #menu.addMenu(submenu)

        # add actions
        menu.addActions([
            paste_action,
            select_all_action,
            undo_action
        ])

        # add separator
        menu.addSeparator()

        # show menu
        menu.exec(e.globalPos(), aniType=MenuAnimationType.FADE_IN_PULL_UP)

    def copy_text(self):
        self.copy()


class TabInterface(QFrame):
    """ Tab interface """

    def __init__(self, text: str, icon, objectName, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(icon, self)
        #self.label = SubtitleLabel(text, self)
        self.iconWidget.setFixedSize(120, 120)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setSpacing(30)
        #self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        #self.vBoxLayout.addWidget(TWidget(), 0)  # Create an instance of TWidget and add it to the TabInterface
        #setFont(self.label, 24)

        self.setObjectName(objectName)


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        # add buttons
        self.toolButtonLayout = QHBoxLayout()
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.menuButton = TransparentToolButton(FIF.MENU, self)
        self.forwardButton = TransparentToolButton(FIF.RIGHT_ARROW.icon(color=color), self)
        self.backButton = TransparentToolButton(FIF.LEFT_ARROW.icon(color=color), self)

        #self.openButton = TransparentToolButton(QIcon("resource/open.png"), self)
        #self.openButton.clicked.connect(parent.open_document)
        #self.newButton = TransparentToolButton(QIcon("resource/new.png"), self)
        #self.newButton.clicked.connect(parent.onTabAddRequested)
        #self.saveButton = TransparentToolButton(QIcon("resource/save.png"), self)
        #self.saveButton.clicked.connect(parent.save_document)

        self.forwardButton.setDisabled(True)
        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.menuButton)
        self.toolButtonLayout.addWidget(self.backButton)
        self.toolButtonLayout.addWidget(self.forwardButton)

        #self.toolButtonLayout.addWidget(self.openButton)
        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)

        # add tab bar
        self.tabBar = TabBar(self)

        self.tabBar.setMovable(True)
        self.tabBar.setTabMaximumWidth(220)
        self.tabBar.setTabShadowEnabled(False)
        self.tabBar.setTabSelectedBackgroundColor(QColor(255, 255, 255, 125), QColor(255, 255, 255, 50))
        self.tabBar.setScrollable(True)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)

        self.tabBar.tabCloseRequested.connect(self.tabBar.removeTab)
        #self.tabBar.currentChanged.connect(lambda i: print(self.tabBar.tabText(i)))

        self.hBoxLayout.insertWidget(5, self.tabBar, 1)
        self.hBoxLayout.setStretch(6, 0)

        #self.hBoxLayout.insertWidget(7, self.saveButton, 0, Qt.AlignmentFlag.AlignLeft)
        #self.hBoxLayout.insertWidget(7, self.openButton, 0, Qt.AlignmentFlag.AlignLeft)
        #self.hBoxLayout.insertWidget(7, self.newButton, 0, Qt.AlignmentFlag.AlignLeft)
        #self.hBoxLayout.insertSpacing(8, 20)

        self.menu = RoundMenu("Menu")
        self.menu.setStyleSheet("QMenu{color : red;}")

        file_menu = RoundMenu("File", self)
        new_action = QAction(text="New", icon=FIF.ADD.icon(QColor("white")))
        new_action.triggered.connect(parent.onTabAddRequested)
        file_menu.addAction(new_action)
        open_action = Action(text="Open", icon=FIF.SEND_FILL)
        open_action.triggered.connect(parent.open_document)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        save_action = Action(text="Save", icon=FIF.SAVE)
        save_action.triggered.connect(parent.save_document)
        file_menu.addAction(save_action)

        self.menu.addMenu(file_menu)

        # Create the menuButton
        #self.menuButton = TransparentToolButton(FIF.MENU, self)
        self.menuButton.clicked.connect(self.showMenu)

    def showMenu(self):
        # Show the menu at the position of the menuButton
        self.menu.exec(self.menuButton.mapToGlobal(self.menuButton.rect().bottomLeft()))

    def canDrag(self, pos: QPoint):
        if not super().canDrag(pos):
            return False

        pos.setX(pos.x() - self.tabBar.x())
        return not self.tabBar.tabRegion().contains(pos)

    def test(self):
        print("hello")


class Window(MSFluentWindow):

    def __init__(self):
        self.isMicaEnabled = True
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))
        self.tabBar = self.titleBar.tabBar  # type: TabBar


        setTheme(Theme.DARK)
        setThemeColor(QColor("red")) #sets the red accents

        # create sub interface
        self.homeInterface = QStackedWidget(self, objectName='homeInterface')
        #self.settingsInterface = Widget('Application Interface', self)
        #self.videoInterface = Widget('Video Interface', self)
        #self.libraryInterface = Widget('library Interface', self)

        self.tabBar.addTab(text="Glyph 1", routeKey="Glyph 1")
        self.tabBar.setCurrentTab('Glyph 1')

        #self.current_editor = self.text_widgets["Scratch 1"]

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, QIcon("resource/write.svg"), 'Write', QIcon("resource/write.svg"))
        #self.addSubInterface(self.appInterface, FIF.ALBUM, '应用')
        #self.addSubInterface(self.videoInterface, FIF.EMBED, '视频')

       # self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF,
       #                      '库', FIF.LIBRARY_FILL, NavigationItemPosition.BOTTOM)
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.INFO,
            text='About',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(
            self.homeInterface.objectName())

        self.text_widgets = {}  # Create a dictionary to store TWidget instances for each tab
        for i in range(self.tabBar.count()):  # Iterate through the tabs using count
            routeKey = self.tabBar.tabText(i)  # Get the routeKey from tabText

            # Create a new instance of TWidget for each tab
            t_widget = TWidget(self)
            self.text_widgets[routeKey] = t_widget  # Store the TWidget instance in the dictionary

            self.current_editor = t_widget

            # Add the TWidget to the corresponding TabInterface
            tab_interface = TabInterface(self.tabBar.tabText(i), 'icon', routeKey, self)
            tab_interface.vBoxLayout.addWidget(t_widget)
            self.homeInterface.addWidget(tab_interface)

        self.tabBar.currentChanged.connect(self.onTabChanged)
        self.tabBar.tabAddRequested.connect(self.onTabAddRequested)

    def initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/icon.ico'))
        self.setWindowTitle('Notes(1)')

#        desktop = QApplication.desktop().availableGeometry()
        w, h = 1200, 800
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def showMessageBox(self):
        w = MessageBox(
            'Notes(1) 📝',
            (
                    "Version : 1.0"
                    + "\n" + "\n" + "\n" + "💝  I hope you'll enjoy using notes(1) as much as I did while coding it  💝" + "\n" + "\n" + "\n" +
                    "Made with 💖 By Rohan Kishore"
            ),
            self
        )
        w.yesButton.setText('GitHub')
        w.cancelButton.setText('Return')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/rohankishore/"))

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.homeInterface.setCurrentWidget(self.findChild(TabInterface, objectName))
        self.stackedWidget.setCurrentWidget(self.homeInterface)

        # Get the currently active tab
        current_tab = self.homeInterface.widget(index)

        if current_tab and isinstance(current_tab, TabInterface):
            # Update the current TWidget
            self.current_editor = self.text_widgets[current_tab.objectName()]


    def onTabAddRequested(self):
        text = f'Glyph {self.tabBar.count() + 1}'
        self.addTab(text, text, '')

        # Set the current_editor to the newly added TWidget
        self.current_editor = self.text_widgets[text]


    def open_document(self):
        file_dir = filedialog.askopenfilename(
            title="Select file",
        )
        filename = os.path.basename(file_dir).split('/')[-1]

        if file_dir:
            try:
                f = open(file_dir, "r")
                filedata = f.read()
                self.addTab(filename, filename, '')
                self.current_editor.setPlainText(filedata)
                f.close()
            except UnicodeDecodeError:
                messagebox.showerror("Wrong Filetype!", "This file type is not supported!")

    def save_document(self):
        try:
            if not self.current_editor:
                print("No active TWidget found.")
                return  # Check if there is an active TWidget

            text_to_save = self.current_editor.toPlainText()
            print("Text to save:", text_to_save)  # Debug print

            name = filedialog.asksaveasfilename(
                title="Select file",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )

            print("File path to save:", name)  # Debug print

            if name:
                with open(name, 'w') as file:
                    file.write(text_to_save)
                    title = os.path.basename(name) + " ~ ZenNotes"
                    active_tab_index = self.tabBar.currentIndex()
                    self.tabBar.setTabText(active_tab_index, os.path.basename(name))
                    self.setWindowTitle(title)
                    print("File saved successfully.")  # Debug print
        except Exception as e:
            print(f"An error occurred while saving the document: {e}")


    def addTab(self, routeKey, text, icon):
        self.tabBar.addTab(routeKey, text, icon)
        self.homeInterface.addWidget(TabInterface(text, icon, routeKey, self))
        # Create a new TWidget instance for the new tab
        t_widget = TWidget(self)
        self.text_widgets[routeKey] = t_widget  # Store the TWidget instance in the dictionary
        tab_interface = self.findChild(TabInterface, routeKey)
        tab_interface.vBoxLayout.addWidget(t_widget)
        self.current_editor = t_widget# Add TWidget to the corresponding TabInterface



if __name__ == '__main__':
    font = QFont("DotNess", 12)
    app = QApplication()
    app.setFont(font)
    w = Window()
    w.setStyleSheet("background-color : black;")
    w.show()
    app.exec()
