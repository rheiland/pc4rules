"""
Authors:
Randy Heiland (heiland@iu.edu)
Dr. Paul Macklin (macklinp@iu.edu)

--- Versions ---
0.1 - initial version
"""
# https://doc.qt.io/qtforpython/gettingstarted.html

import os
import sys
# import getopt
import argparse
import shutil
import glob
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
from xml.dom import minidom

# from matplotlib.colors import TwoSlopeNorm

from PyQt5 import QtGui   # , QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QProcess
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QFont

from about_tab import About
from config_tab import Config
from populate_tree_cell_defs import populate_tree_cell_defs
from cell_def_tab import CellDef 
from microenv_tab import SubstrateDef 
from user_params_tab import UserParams 
from ics_tab import ICs 
from rules_tab import Rules 
from run_tab import RunModel 
from vis_tab import Vis 
from legend_tab import Legend 


class QHLine(QFrame):
    def __init__(self, sunken_flag):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameStyle(QFrame.NoFrame)
        if sunken_flag:
            self.setFrameShadow(QFrame.Sunken)

def SingleBrowse(self):
        # if len(self.csv) < 2:
    filePath = QFileDialog.getOpenFileName(self,'',".",'*.xml')

        #     if filePath != "" and not filePath in self.csv:
        #         self.csv.append(filePath)
        # print(self.csv)
  
#class PhysiCellXMLCreator(QTabWidget):
class PhysiCellXMLCreator(QWidget):
    # def __init__(self, parent = None):
    # ex = PhysiCellXMLCreator(vis_flag, config_file, skip_validate_flag, exec_file)
    def __init__(self, show_vis_flag, config_file, skip_validate_flag, exec_file_flag, parent = None):
        super(PhysiCellXMLCreator, self).__init__(parent)

        # self.rules_plot = RulesPlotWindow()
        # self.window1.show()

        # self.nanohub = True
        self.studio_flag = True
        self.nanohub_flag = False
        if( 'HOME' in os.environ.keys() ):
            self.nanohub_flag = "home/nanohub" in os.environ['HOME']

        self.p = None # Necessary to download files!

        # self.title_prefix = "PhysiCell Studio: "
        self.title_prefix = "pc4rules: "
        # self.title_prefix = "PhysiCell Studio"
        self.setWindowTitle(self.title_prefix)

        # Menus
        vlayout = QVBoxLayout(self)
        # vlayout.setContentsMargins(5, 35, 5, 5)  # left,top,right,bottom
        vlayout.setContentsMargins(-1, 10, -1, -1)
        # if not self.nanohub_flag:
        if True:
            menuWidget = QWidget(self.menu())
            vlayout.addWidget(menuWidget)
            vlayout.addWidget(QHLine(False))
        # self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_DialogNoButton')))
        # self.setWindowIcon(QtGui.QIcon('physicell_logo_25pct.png'))
        icon_path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'physicell_logo_200px.png')
        print("icon_path= ",icon_path)
        self.setWindowIcon(QIcon(icon_path))

        # self.grid = QGridLayout()
        # lay.addLayout(self.grid)
        self.setLayout(vlayout)

        self.resize(1100, 770)  # width, height (height >= Cell Types|Death params)
        self.setMinimumSize(1100, 770)  # width, height (height >= Cell Types|Death params)
        # self.setMinimumSize(1200, 770)  # width, height (height >= Cell Types|Death params)

        # self.menubar = QtWidgets.QMenuBar(self)
        # self.file_menu = QtWidgets.QMenu('File')
        # self.file_menu.insertAction("Open")
        # self.menubar.addMenu(self.file_menu)

        # model_name = "rules_model1"
        # model_name = "template"
        model_name = "tumor"

        # then what??
        # binDirectory = os.path.realpath(os.path.abspath(__file__))
        self.current_dir = os.getcwd()
        print("self.current_dir = ",self.current_dir)
        self.studio_root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.studio_data_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        print("self.studio_root_dir = ",self.studio_root_dir)

        # assume running from a PhysiCell root dir, but change if not
        self.config_dir = os.path.realpath(os.path.join('.', 'config'))

        if self.current_dir == self.studio_root_dir:  # are we running from Studio root dir?
            self.config_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        print(f'self.config_dir =  {self.config_dir}')

        #-----
        # binDirectory = os.path.dirname(os.path.abspath(__file__))
        # dataDirectory = os.path.join(binDirectory,'..','data')
        # print("-------- dataDirectory (relative) =",dataDirectory)
        # self.absolute_data_dir = os.path.abspath(dataDirectory)

        self.absolute_data_dir = os.path.abspath(self.studio_data_dir)
        print("-------- absolute_data_dir =",self.absolute_data_dir)

        # NOTE: if your C++ needs to also have an absolute path to data dir, do so via an env var
        # os.environ['KIDNEY_DATA_PATH'] = self.absolute_data_dir

        # docDirectory = os.path.join(binDirectory,'..','doc')
        docDirectory = os.path.join(self.studio_root_dir,'doc')
        self.absolute_doc_dir = os.path.abspath(docDirectory)
        print("-------- absolute_doc_dir =",self.absolute_doc_dir)


        #--------------------------
        if config_file:
            self.current_xml_file = os.path.join(self.current_dir, config_file)
            print("got config_file=",config_file)
            # sys.exit()
        else:
            # model_name = "rules_model1"
            model_name = "tumor"
            read_file = os.path.join(self.absolute_data_dir, model_name + ".xml")
            self.current_xml_file = os.path.join(self.studio_data_dir, model_name + ".xml")
        #--------------------------

        # read_file = model_name + ".xml"
        # read_file = os.path.join(dataDirectory, model_name + ".xml")
        # self.setWindowTitle(self.title_prefix + model_name)


        if self.nanohub_flag:
            # NOTE! We create a *copy* of the .xml sample model and will save to it.
            copy_file = "copy_" + model_name + ".xml"
            shutil.copy(read_file, copy_file)
            # self.setWindowTitle(self.title_prefix + "pc4learning")
            self.setWindowTitle(self.title_prefix + copy_file)
            self.config_file = copy_file  # to Save
        else:
            # self.setWindowTitle(self.title_prefix + copy_file)
            self.setWindowTitle(self.title_prefix + self.current_xml_file)
            self.config_file = self.current_xml_file  # to Save
            # self.setWindowTitle(self.title_prefix + "pc4learning")
        # self.add_new_model(copy_file, True)
        # self.config_file = "config_samples/" + name + ".xml"
        print("-----  __init__():  self.config_file = ",self.config_file)


        # self.config_file = read_file  # nanoHUB... to Save
        # self.tree = ET.parse(self.config_file)
        # fp = open(self.config_file)
        # self.tree = ET.parse(fp)
        # fp.close()

        with open(self.config_file, 'r') as xml_file:
            self.tree = ET.parse(xml_file)

        # tree = ET.parse(read_file)
        # self.tree = ET.parse(read_file)
        self.xml_root = self.tree.getroot()

        # self.about_tab = About(self.nanohub_flag)
        self.about_tab = About(self.absolute_doc_dir, self.nanohub_flag)

        # self.template_cb()

        # self.num_models = 0
        # self.model = {}  # key: name, value:[read-only, tree]

        self.config_tab = Config(self.nanohub_flag)
        self.config_tab.xml_root = self.xml_root
        self.config_tab.fill_gui()
        self.output_dir = self.config_tab.folder.text()
        print("studio.py: self.output_dir=",self.output_dir)

        self.microenv_tab = SubstrateDef()
        self.microenv_tab.xml_root = self.xml_root
        substrate_name = self.microenv_tab.first_substrate_name()
        print("studio.py: substrate_name=",substrate_name)
        self.microenv_tab.populate_tree()  # rwh: both fill_gui and populate_tree??

        # self.tab2.tree.setCurrentItem(QTreeWidgetItem,0)  # item

        self.dark_mode = False
        self.celldef_tab = CellDef(self.dark_mode)
        self.celldef_tab.xml_root = self.xml_root
        cd_name = self.celldef_tab.first_cell_def_name()
        print("studio.py: cd_name=",cd_name)
        self.skip_validate = False
        populate_tree_cell_defs(self.celldef_tab, self.skip_validate)
        # self.celldef_tab.populate_tree()
        self.celldef_tab.fill_substrates_comboboxes()
        self.celldef_tab.fill_celltypes_comboboxes()
        # self.vis_tab.substrates_cbox_changed_cb(2)
        self.microenv_tab.celldef_tab = self.celldef_tab

        # self.cell_customdata_tab = CellCustomData()
        # self.cell_customdata_tab.xml_root = self.xml_root
        # self.cell_customdata_tab.celldef_tab = self.celldef_tab
        # self.cell_customdata_tab.fill_gui(self.celldef_tab)
        # self.celldef_tab.fill_custom_data_tab()
        
        self.user_params_tab = UserParams(self.dark_mode)
        self.user_params_tab.xml_root = self.xml_root
        self.user_params_tab.fill_gui()

        self.ics_tab = ICs(self.config_tab, self.celldef_tab)
        self.ics_tab.fill_celltype_combobox()
        self.ics_tab.reset_info()
        self.celldef_tab.ics_tab = self.ics_tab
        # self.rules_tab.fill_gui()


        # self.rules_tab = Rules(self.absolute_doc_dir, self.nanohub_flag)
        self.rules_tab = Rules(self.microenv_tab, self.celldef_tab)
        self.rules_tab.xml_root = self.xml_root
        self.rules_tab.fill_gui()
        self.celldef_tab.rules_tab = self.rules_tab
        # populate_tree_cell_defs(self.celldef_tab, self.rules_tab, self.skip_validate)
        uep_cell_rules = self.xml_root.find(".//cell_definitions//cell_rules")
        if uep_cell_rules:
            rules_folder = uep_cell_rules.find(".//folder").text 
            rules_file = uep_cell_rules.find(".//filename").text 
            # logging.debug(f'------- studio.py: setting rules.csv folder = {rules_folder}')
            # logging.debug(f'------- studio.py: setting rules.csv file = {rules_file}')
            print(f'------- studio.py: setting rules.csv folder = {rules_folder}')
            print(f'------- studio.py: setting rules.csv file = {rules_file}')
            if rules_folder and rules_file:
                full_path_rules_name =  os.path.realpath(os.path.join(self.studio_root_dir, rules_folder, rules_file))
                print(f'------- studio.py: full_path_rules_name = {full_path_rules_name}')
                self.rules_tab.fill_rules(full_path_rules_name)
            else:
                print(f'------- studio.py: WARNING: missing either rules_folder or rules_file.')

        self.tabWidget = QTabWidget()

        self.download_menu = None
        self.rules_flag = True
        self.run_tab = RunModel(self.nanohub_flag, self.tabWidget, self.rules_flag, self.download_menu)
        self.homedir = os.getcwd()
        print("studio.py: self.homedir = ",self.homedir)
        self.run_tab.homedir = self.homedir
        self.run_tab.rules_tab = self.rules_tab
        self.rules_tab.homedir = self.homedir
        if not self.nanohub_flag:
            self.run_tab.config_file = self.config_file
            self.run_tab.config_xml_name.setText(self.config_file)
        # self.run_tab.nanohub_flag = self.nanohub_flag

        # self.run_tab.xmin = 
        # self.run_tab.xmax = 

        #------------------
        # if self.nanohub_flag:  # to be able to fill_xml() from Run tab
        if True:  # to be able to fill_xml() from Run tab
            self.run_tab.config_tab = self.config_tab
            self.run_tab.microenv_tab = self.microenv_tab 
            self.run_tab.celldef_tab = self.celldef_tab
            self.run_tab.user_params_tab = self.user_params_tab
            self.run_tab.tree = self.tree

        #------------------
        # self.tabWidget = QTabWidget()
        stylesheet = """
            QTabBar::tab:selected {background: orange;}   #  dodgerblue
            """
        self.tabWidget.setStyleSheet(stylesheet)
        self.tabWidget.addTab(self.about_tab,"About")
        self.tabWidget.addTab(self.config_tab,"Config Basics")
        self.tabWidget.addTab(self.microenv_tab,"Microenvironment")
        self.tabWidget.addTab(self.celldef_tab,"Cell Types")
        self.tabWidget.addTab(self.user_params_tab,"User Params")
        self.tabWidget.addTab(self.ics_tab,"ICs")
        self.tabWidget.addTab(self.rules_tab,"Rules")
        self.tabWidget.addTab(self.run_tab,"Run")

        if show_vis_flag:
            print("studio.py: creating vis_tab (Plot tab) and legend_tab")
            self.vis_tab = Vis(self.nanohub_flag)
            self.vis_tab.output_folder.setText(self.output_dir)
            # self.vis_tab.output_dir = self.output_dir
            # self.vis_tab.reset_plot_range()

            self.legend_tab = Legend(self.nanohub_flag)
            self.legend_tab.output_dir = self.output_dir
            # self.vis_tab.setEnabled(False)
            # self.vis_tab.nanohub_flag = self.nanohub_flag
            # self.vis_tab.xml_root = self.xml_root
            self.tabWidget.addTab(self.vis_tab,"Plot")
            # self.tabWidget.setTabEnabled(5, False)

            self.tabWidget.addTab(self.legend_tab,"Legend")

            self.run_tab.vis_tab = self.vis_tab
            self.run_tab.legend_tab = self.legend_tab
            print("studio.py: calling vis_tab.substrates_cbox_changed_cb(2)")
            self.vis_tab.fill_substrates_combobox(self.celldef_tab.substrate_list)
            # self.vis_tab.substrates_cbox_changed_cb(2)   # doesn't accomplish it; need to set index, but not sure when
            self.vis_tab.init_plot_range(self.config_tab)
            self.vis_tab.show_edge = False

            self.vis_tab.output_dir = self.output_dir


        vlayout.addWidget(self.tabWidget)
        # self.addTab(self.sbml_tab,"SBML")

        # self.tabWidget.setCurrentIndex(1)  # rwh/debug: select Microenv
        # self.tabWidget.setCurrentIndex(2)  # rwh/debug: select Cell Types
        if show_vis_flag:
            self.tabWidget.setCurrentIndex(0)    # About
        else:
            self.tabWidget.setCurrentIndex(0)  # About

        # self.tabWidget.setCurrentIndex(5)  # rwh hack/debug/default
        # self.tabWidget.setCurrentIndex(7)  # Run
        # self.tabWidget.setCurrentIndex(8)  # Plot


        # self.reset_xml_root()

    #-----------------------------------------
    def about_pyqt(self):
        msgBox = QMessageBox()
        msgBox.setTextFormat(Qt.RichText)
        about_text = """ 
PhysiCell Studio is developed using PyQt5.<br><br>

For licensing information:<br>
<a href="https://github.com/PyQt5/PyQt/blob/master/LICENSE">github.com/PyQt5/PyQt/blob/master/LICENSE</a>

        """
        msgBox.setText(about_text)
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()

    def about_studio(self):
        msgBox = QMessageBox()
        # font = QFont()
        # font.setBold(True)
        # msgBox.setFont(font)
        msgBox.setTextFormat(Qt.RichText)
        # msgBox.setIcon(QMessageBox.Information)
        version_file =  os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'VERSION.txt'))
        try:
            with open(version_file) as f:
                v = f.readline()
        except:
            v = "(can't find VERSION.txt)\n"
            print("Unable to open ",version_file)
        about_text = "Version " + v + """ <br><br>
PhysiCell Studio is a tool to provide graphical editing of a PhysiCell model and, optionally, run a model and visualize results. &nbsp; It is lead by the Macklin Lab (Indiana University) with contributions from the PhysiCell community.<br><br>

NOTE: When loading a model (.xml configuration file), it must be a "flat" format for the  cell_definitions, i.e., all parameters need to be defined. &nbsp; Many legacy PhysiCell models used a hierarchical format in which a cell_definition could inherit from a parent. &nbsp; The hierarchical format is not supported in the Studio.<br><br>

For more information:<br>
<a href="https://github.com/PhysiCell-Tools/PhysiCell-model-builder">github.com/PhysiCell-Tools/PhysiCell-model-builder</a><br>
<a href="https://github.com/MathCancer/PhysiCell">https://github.com/MathCancer/PhysiCell</a><br>
<br>
PhysiCell Studio is provided "AS IS" without warranty of any kind. &nbsp; In no event shall the Authors be liable for any damages whatsoever.<br>
        """
        msgBox.setText(about_text)
        # msgBox.setInformativeText(about_text)
        # msgBox.setDetailedText(about_text)
        # msgBox.setText("PhysiCell Studio is a tool to provide easy editing of a PhysiCell model and, optionally, run a model and visualize results.")
        msgBox.setStandardButtons(QMessageBox.Ok)
        # msgBox.buttonClicked.connect(msgButtonClick)

        returnValue = msgBox.exec()

    #-----------------------------------------
    def enablePlotTab(self, bval):
        # self.tabWidget.setTabEnabled(5, bval)
        self.tabWidget.setTabEnabled(6, bval)   # tab index = 6 if About tab is defined

    def enableLegendTab(self, bval):
        self.tabWidget.setTabEnabled(7, bval)   

    def menu(self):
        menubar = QMenuBar(self)
        menubar.setNativeMenuBar(False)

        #--------------
        studio_menu = menubar.addMenu('&Studio')
        studio_menu.addAction("About", self.about_studio)
        studio_menu.addAction("About PyQt", self.about_pyqt)
        # studio_menu.addAction("Preferences", self.prefs_cb)
        studio_menu.addSeparator()
        studio_menu.addAction("Quit", quit_cb)

        #--------------
        file_menu = menubar.addMenu('&File')
        # file_menu.addAction("Save as mymodel.xml", self.save_as_cb) 

        if not self.nanohub_flag: 
            file_menu.addAction("Open", self.open_as_cb, QtGui.QKeySequence('Ctrl+o'))
            # file_menu.addAction("Save mymodel.xml", self.save_cb, QtGui.QKeySequence('Ctrl+s'))
            file_menu.addAction("Save as", self.save_as_cb)
            file_menu.addAction("Save", self.save_cb, QtGui.QKeySequence('Ctrl+s'))

            #--------------
            # export_menu = file_menu.addMenu("Export")

            # simularium_act = QAction('Simularium', self)
            # export_menu.addAction(simularium_act)
            # simularium_act.triggered.connect(self.simularium_cb)
            # if not self.studio_flag:
            #     print("simularium_installed is ",simularium_installed)
            #     export_menu.setEnabled(False)

            # #--------------
            # file_menu.addSeparator()
            # samples_menu = file_menu.addMenu("Samples")

            # template_act = QAction('template', self)
            # samples_menu.addAction(template_act)
            # template_act.triggered.connect(self.template_cb)

            self.download_menu = None

        # if self.nanohub_flag: 
        else:  # rwh: temporary
            self.download_menu = file_menu.addMenu('Download')
            self.download_config_item = self.download_menu.addAction("Download config.xml", self.download_config_cb)
            self.download_svg_item = self.download_menu.addAction("Download SVG", self.download_svg_cb)
            self.download_mat_item = self.download_menu.addAction("Download binary (.mat) data", self.download_full_cb)
            # self.download_menu_item.setEnabled(False)
            self.download_menu.setEnabled(False)

        #-----
        # model_menu = menubar.addMenu('&Model')

        # # open_act = QtGui.QAction('Open', self, checkable=True)
        # # open_act = QtGui.QAction('Open', self)
        # # open_act.triggered.connect(self.open_as_cb)
        # # file_menu.addAction("New (template)", self.new_model_cb, QtGui.QKeySequence('Ctrl+n'))
        # model_menu.addAction("template", self.template_cb)
        # model_menu.addAction("biorobots", self.biorobots_cb)
        # model_menu.addAction("celltypes3", self.celltypes3_cb)
        # model_menu.addAction("pred_prey_farmer", self.pred_prey_cb)
        # model_menu.addAction("interactions", self.interactions_cb)

        #-----
        # view_menu = menubar.addMenu('&View')
        # view_menu.addAction("Show/Hide plot range", self.view_plot_range_cb)

        menubar.adjustSize()  # Argh. Otherwise, only 1st menu appears, with ">>" to others!

    #-----------------------------------------------------------------
    def message(self, s):
        # self.text.appendPlainText(s)
        print(s)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Download process finished.")
        print("-- download finished.")
        self.p = None

    def download_config_cb(self):
        if self.nanohub_flag:
            if self.p is None:  # No process running.
                self.p = QProcess()
                self.p.readyReadStandardOutput.connect(self.handle_stdout)
                self.p.readyReadStandardError.connect(self.handle_stderr)
                self.p.stateChanged.connect(self.handle_state)
                self.p.finished.connect(self.process_finished)  # Clean up once complete.

                self.p.start("exportfile config.xml")
        return

    def download_svg_cb(self):
        if self.nanohub_flag:
            if self.p is None:  # No process running.
                self.p = QProcess()
                self.p.readyReadStandardOutput.connect(self.handle_stdout)
                self.p.readyReadStandardError.connect(self.handle_stderr)
                self.p.stateChanged.connect(self.handle_state)
                self.p.finished.connect(self.process_finished)  # Clean up once complete.

                # file_str = os.path.join(self.output_dir, '*.svg')
                file_str = "*.svg"
                print('-------- download_svg_cb(): zip up all ',file_str)
                with zipfile.ZipFile('svg.zip', 'w') as myzip:
                    for f in glob.glob(file_str):
                        myzip.write(f, os.path.basename(f))   # 2nd arg avoids full filename 
                self.p.start("exportfile svg.zip")
        return

    def download_full_cb(self):
        if self.nanohub_flag:
            if self.p is None:  # No process running.
                self.p = QProcess()
                self.p.readyReadStandardOutput.connect(self.handle_stdout)
                self.p.readyReadStandardError.connect(self.handle_stderr)
                self.p.stateChanged.connect(self.handle_state)
                self.p.finished.connect(self.process_finished)  # Clean up once complete.

                # file_xml = os.path.join(self.output_dir, '*.xml')
                # file_mat = os.path.join(self.output_dir, '*.mat')
                file_xml = '*.xml'
                file_mat = '*.mat'
                print('-------- download_full_cb(): zip up all .xml and .mat')
                with zipfile.ZipFile('mcds.zip', 'w') as myzip:
                    for f in glob.glob(file_xml):
                        myzip.write(f, os.path.basename(f)) # 2nd arg avoids full filename path in the archive
                    for f in glob.glob(file_mat):
                        myzip.write(f, os.path.basename(f))
                self.p.start("exportfile mcds.zip")
        return


    def reset_xml_root(self):
        self.celldef_tab.param_d.clear()  # seems unnecessary as being done in populate_tree. argh.
        self.celldef_tab.clear_custom_data_tab()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("reset_xml_root(): after celldef_tab.param_d.clear(), param_d = ", self.celldef_tab.param_d)
        self.celldef_tab.current_cell_def = None
        # self.microenv_tab.param_d.clear()

        self.xml_root = self.tree.getroot()
        self.config_tab.xml_root = self.xml_root
        self.microenv_tab.xml_root = self.xml_root
        self.celldef_tab.xml_root = self.xml_root
        # self.cell_customdata_tab.xml_root = self.xml_root
        self.user_params_tab.xml_root = self.xml_root
        # self.run_tab.xml_root = self.xml_root

        # --------Now fill all tabs' params------
        self.config_tab.fill_gui()

        self.microenv_tab.clear_gui()
        self.microenv_tab.populate_tree()
        # self.microenv_tab.fill_gui(None)
        # self.microenv_tab.fill_gui()

        # Do this before the celldef_tab
        # self.cell_customdata_tab.clear_gui(self.celldef_tab)
        # self.cell_customdata_tab.fill_gui(self.celldef_tab)

        # self.celldef_tab.clear_gui()
        self.celldef_tab.clear_custom_data_params()
        # self.celldef_tab.populate_tree()
        populate_tree_cell_defs(self.celldef_tab, self.skip_validate)
        # populate_tree_cell_defs(self.celldef_tab, self.rules_tab, self.skip_validate)
        # self.celldef_tab.fill_gui(None)
        # self.celldef_tab.customize_cycle_choices() #rwh/todo: needed? 
        self.celldef_tab.fill_substrates_comboboxes()
        self.celldef_tab.fill_celltypes_comboboxes()

        self.microenv_tab.celldef_tab = self.celldef_tab

        # self.cell_customdata_tab.clear_gui(self.celldef_tab)
        # self.cell_customdata_tab.fill_gui(self.celldef_tab)

        self.user_params_tab.clear_gui()
        self.user_params_tab.fill_gui()

        self.rules_tab.fill_gui()
        uep_cell_rules = self.xml_root.find(".//cell_definitions//cell_rules")
        if uep_cell_rules:
            rules_folder = uep_cell_rules.find(".//folder").text 
            rules_file = uep_cell_rules.find(".//filename").text 
            # logging.debug(f'------- studio.py: setting rules.csv folder = {rules_folder}')
            # logging.debug(f'------- studio.py: setting rules.csv file = {rules_file}')
            print(f'------- studio.py: setting rules.csv folder = {rules_folder}')
            print(f'------- studio.py: setting rules.csv file = {rules_file}')

        self.vis_tab.init_plot_range(self.config_tab)
        self.vis_tab.reset_model()
        # self.output_dir = self.config_tab.folder.text()
        self.vis_tab.output_dir = self.config_tab.folder.text()
        self.vis_tab.output_folder.setText(self.vis_tab.output_dir)
        print("\nstudio.py: reset_xml_root(): vis_tab.output_folder.setText=",self.vis_tab.output_dir)
        # self.vis_tab.setEnabled(False)
        self.enablePlotTab(True)

        self.enableLegendTab(True)
        self.tabWidget.setCurrentIndex(0)  # Config (default)


    def show_sample_model(self):
        # logging.debug(f'pmb: show_sample_model(): self.config_file = {self.config_file}')
        print(f'studio.py: show_sample_model(): self.config_file = {self.config_file}')
        # self.config_file = "config_samples/biorobots.xml"
        self.tree = ET.parse(self.config_file)
        # self.xml_root = self.tree.getroot()
        self.reset_xml_root()
        self.setWindowTitle(self.title_prefix + self.config_file)
        # self.config_tab.fill_gui(self.xml_root)  # 
        # self.microenv_tab.fill_gui(self.xml_root)  # microenv
        # self.celldef_tab.fill_gui("foobar")  # cell defs
        # self.celldef_tab.fill_motility_substrates()


    def open_as_cb(self):
        # filePath = QFileDialog.getOpenFileName(self,'',".",'*.xml')
        filePath = QFileDialog.getOpenFileName(self,'',".")
        # print("\n\nopen_as_cb():  filePath=",filePath)
        full_path_model_name = filePath[0]
        print("\n\nopen_as_cb():  full_path_model_name =",full_path_model_name )
        # logging.debug(f'\npmb.py: open_as_cb():  full_path_model_name ={full_path_model_name}')
        # if (len(full_path_model_name) > 0) and Path(full_path_model_name):
        if (len(full_path_model_name) > 0) and Path(full_path_model_name).is_file():
            print("open_as_cb():  filePath is valid")
            # logging.debug(f'     filePath is valid')
            print("len(full_path_model_name) = ", len(full_path_model_name) )
            # logging.debug(f'     len(full_path_model_name) = {len(full_path_model_name)}' )
            # fname = os.path.basename(full_path_model_name)
            self.current_xml_file = full_path_model_name

            # self.add_new_model(self.current_xml_file, True)
            self.config_file = self.current_xml_file

            # -- don't do this now; file is copied to tmpdir/config.xml
            # if self.studio_flag:
            if not self.nanohub_flag:
                self.run_tab.config_file = self.current_xml_file
                self.run_tab.config_xml_name.setText(self.current_xml_file)
            self.show_sample_model()

        else:
            print("open_as_cb():  full_path_model_name is NOT valid")

    # Only valid for desktop, not on nanoHUB
    def save_as_cb(self):
        save_as_file = QFileDialog.getSaveFileName(self,'',".")
        if save_as_file:
            print(" save_as_file= ",save_as_file) # writing to:  ('/Users/heiland/git/PhysiCell-model-builder/rwh.xml', 'All Files (*)')

        self.config_tab.fill_xml()
        self.microenv_tab.fill_xml()
        self.celldef_tab.fill_xml()
        self.user_params_tab.fill_xml()

        # save_as_file = "mymodel.xml"
        print("studio.py:  save_as_cb: writing to: ",save_as_file) # writing to:  ('/Users/heiland/git/PhysiCell-model-builder/rwh.xml', 'All Files (*)')
        self.tree.write(save_as_file[0])

    def view_plot_range_cb(self):
        self.vis_tab.show_hide_plot_range()

    def indent(elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="",  newl="")  # newl="\n"

    def save_cb(self):
        # self.config_file = copy_file
        self.config_tab.fill_xml()
        self.microenv_tab.fill_xml()
        self.celldef_tab.fill_xml()
        self.user_params_tab.fill_xml()
        self.rules_tab.fill_xml()

        # filePath = QFileDialog.getOpenFileName(self,'',".",'*.xml')
        # print("studio.py:  save_cb: writing to: ",self.config_file)

        # out_file = self.config_file
        # out_file = "mymodel.xml"
        print("studio.py:  save_cb: writing to: ",self.config_file)

        # self.tree.write(self.config_file)
        # root = ET.fromstring("<fruits><fruit>banana</fruit><fruit>apple</fruit></fruits>""")
        # tree = ET.ElementTree(root)
        # ET.indent(self.tree)  # ugh, only in 3.9
        # root = ET.tostring(self.tree)
        # self.indent(self.tree)
        # self.indent(root)

        # rwh: ARGH, doesn't work
        # root = self.tree.getroot()
        # out_str = self.prettify(root)
        # print(out_str)

        # self.tree.write(outfile)
        self.tree.write(self.config_file)  # does this close the file??

        # rwh NOTE: after saving the .xml, do we need to read it back in to reflect changes.
        # self.tree = ET.parse(self.config_file)
        # self.xml_root = self.tree.getroot()
        # self.reset_xml_root()

    def load_state_cb(self):
        filePath = QFileDialog.getOpenFileName(self,'',".")
        if len(filePath[0]) > 0:
            print("\n\nload_state_cb():  filePath=",filePath)
            print("len(filePath[0])=",len(filePath[0]))
            full_path_pssm_name = filePath[0]
            pssm_tree = ET.parse(full_path_pssm_name)
            pssm_root = pssm_tree.getroot()
            exec_pgm = pssm_root.find(".//exec").text
            print("exec_pgm = ",exec_pgm)
            config_file = pssm_root.find(".//config").text
            print("config_file = ",config_file)
            self.run_tab.exec_name.setText(exec_pgm)
            self.run_tab.config_file = config_file
            self.run_tab.config_xml_name.setText(config_file)

def quit_cb():
    global studio_app
    studio_app.quit()

def main():
    global studio_app
    inputfile = ''
    # show_vis_tab = True
    vis_flag = True
    config_file = None
    # model3D_flag = False
    # rules_flag = True
    skip_validate_flag = False
    try:
        parser = argparse.ArgumentParser(description='PhysiCell Studio')

        # parser.add_argument("-s", "--studio", "--Studio", help="include Studio tabs", action="store_true")
        # parser.add_argument("-3", "--three", "--3D", help="assume a 3D model" , action="store_true")
        # parser.add_argument("-r", "--rules", "--Rules", help="display Rules tab" , action="store_true")
        parser.add_argument("-x", "--skip_validate", help="do not attempt to validate the config (.xml) file" , action="store_true")
        parser.add_argument("-c", "--config",  type=str, help="config file (.xml)")
        parser.add_argument("-e", "--exec",  type=str, help="executable model")

        exec_file = 'project'  # for template sample; renamed later

        # args = parser.parse_args()
        args, unknown = parser.parse_known_args()
        if unknown:
            print("invalid argument: ",unknown)
            sys.exit(-1)

        if args.skip_validate:
            # logging.debug(f'studio.py: Do not validate the config file (.xml)')
            skip_validate_flag = True

        # print("args.config= ",args.config)
        if args.config:
            # logging.debug(f'studio.py: config file is {args.config}')
            print(f'studio.py: config file is {args.config}')
            # sys.exit()
            config_file = args.config
            # if (len(config_file) > 0) and Path(config_file).is_file():
            #     logging.debug(f'studio.py: open_as_cb():  filePath is valid')
            #     logging.debug(f'len(config_file) = {len(config_file)}')
            #     logging.debug(f'done with args.config')
            # else:
            #     print(f'config_file is NOT valid: {args.config}')
            #     logging.error(f'config_file is NOT valid: {args.config}')
            #     sys.exit()

        if args.exec:
            # logging.debug(f'exec pgm is {args.exec}')
            # sys.exit()
            exec_file = args.exec
            if (len(exec_file) > 0) and Path(exec_file).is_file():
                print("exec_file exists")
            else:
                print("exec_file is NOT valid: ", args.exec)
                sys.exit()
    except:
        print("Error parsing command line args.")
        sys.exit(-1)


    studio_app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'physicell_logo_200px.png')
    studio_app.setWindowIcon(QIcon(icon_path))

    # ex = PhysiCellXMLCreator(config_file, studio_flag, skip_validate_flag, rules_flag, model3D_flag, exec_file)
    ex = PhysiCellXMLCreator(vis_flag, config_file, skip_validate_flag, exec_file)


    # ex.setGeometry(100,100, 800,600)
    ex.show()
    sys.exit(studio_app.exec_())
	
if __name__ == '__main__':
    main()