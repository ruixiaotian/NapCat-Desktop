# -*- coding: utf-8 -*-

"""
构建主窗体
"""

from abc import ABC

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QWidget
from creart import it, add_creator, exists_module
from creart.creator import AbstractCreator, CreateTargetInfo
from loguru import logger
from qfluentwidgets.common import FluentIcon
from qfluentwidgets.components import NavigationItemPosition
from qfluentwidgets.window import MSFluentWindow, SplashScreen

from src.Ui.resource import resource
from src.Ui.MainWindow.TitleBar import CustomTitleBar
from src.Ui.SetupPage import SetupWidget
from src.Ui.HomePage import HomeWidget
from src.Ui.AddPage import AddWidget
from src.Ui.BotListPage import BotListWidget


class MainWindow(MSFluentWindow):

    def __init__(self) -> None:
        """
        程序的主窗体
        """
        super().__init__()
        self.setWindow()
        self.setItem()

        # 组件加载完成结束 SplashScreen
        self.splashScreen.finish()
        logger.success("窗体构建完成")

    def setWindow(self) -> None:
        """
        设置窗体
        """
        # 标题栏部分
        self.setTitleBar(CustomTitleBar(self))
        # 窗体大小以及设置打开时居中
        self.setMinimumSize(900, 560)
        desktop = QApplication.screens()[0].availableGeometry()
        width, height = desktop.width(), desktop.height()
        self.move(width // 2 - self.width() // 2, height // 2 - self.height() // 2)
        # 创建 Splash Screen
        self.splashScreen = SplashScreen(":Global/logo.png", self, True)
        self.splashScreen.setIconSize(QSize(128, 128))
        self.splashScreen.raise_()
        # 显示窗体
        self.show()
        # 挂起
        QApplication.processEvents()
        logger.success("窗体设置完成")

    def setItem(self) -> None:
        """
        设置侧边栏
        """
        self.setup_widget = it(SetupWidget).initialize(self)
        self.home_widget = it(HomeWidget).initialize(self)
        self.add_widget = it(AddWidget).initialize(self)
        self.bot_list_widget = it(BotListWidget).initialize(self)

        # 添加子页面
        self.addSubInterface(
            interface=self.home_widget,
            icon=FluentIcon.HOME,
            text=self.tr("Home"),
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.add_widget,
            icon=FluentIcon.ADD_TO,
            text=self.tr("Add Bot"),
            position=NavigationItemPosition.TOP
        )
        self.addSubInterface(
            interface=self.bot_list_widget,
            icon=FluentIcon.MENU,
            text=self.tr("Bot List"),
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.setup_widget,
            icon=FluentIcon.SETTING,
            text=self.tr("Setup"),
            position=NavigationItemPosition.BOTTOM
        )

        logger.success("侧边栏构建完成")


class MainWindowClassCreator(AbstractCreator, ABC):
    # 定义类方法targets，该方法返回一个元组，元组中包含了一个CreateTargetInfo对象，
    # 该对象描述了创建目标的相关信息，包括应用程序名称和类名。
    targets = (CreateTargetInfo("src.Ui.MainWindow.Window", "MainWindow"),)

    # 静态方法available()，用于检查模块"MainWindow"是否存在，返回值为布尔型。
    @staticmethod
    def available() -> bool:
        return exists_module("src.Ui.MainWindow.Window")

    # 静态方法create()，用于创建MainWindow类的实例，返回值为MainWindow对象。
    @staticmethod
    def create(create_type: [MainWindow]) -> MainWindow:
        return MainWindow()


add_creator(MainWindowClassCreator)
