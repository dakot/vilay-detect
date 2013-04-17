from PyQt4 import QtCore, QtGui

from vilay.core.DescriptionScheme import DescriptionScheme
from vilay.core.Descriptor import Descriptor

class AnnotationTree(QtGui.QTreeWidget):

    def __init__(self, parent = None):
        super(AnnotationTree, self).__init__ (parent)
        
        # main objects
        self.selectedDItems = [] #list of selected Descriptor oder DS items
        #self.actConceptTreeItemType = None
        self.itemDict = dict()
        
        self.vd = None
        
        # context menu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.conceptTreeContextMenu)
        #self.connect(self.ui.treeView,SIGNAL("selectionChanged()"), self.tree_clicked)
        self.connect(self.selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.selectionWasChanged) 

    def getDSelection(self):
        return self.selectedDItems
    
    def selectionWasChanged(self, newSelection, oldSelection):
        if len(self.selectedItems()) > 0:
            self.selectedDItems = list()
            for item in self.selectedItems():
                dItem = self.itemDict.get(item)
                self.selectedDItems.append(dItem)
            self.emit(QtCore.SIGNAL('dSelectionChanged()'))
    
    def dropEvent(self, event):
        if event.source() == self:
            QtGui.QAbstractItemView.dropEvent(self, event)
    
    def dropMimeData(self, parent, index, data, action):
        if isinstance(parent, QtGui.QTreeWidgetItem):
            parentDSItem = self.itemDict.get(parent)
            
            if isinstance(parentDSItem, DescriptionScheme):
                for selDItem in self.selectedDItems:
                    selDItem.move(parentDSItem)
                    # TODO: do just local update
                    self.createObjectTree()
                    return True
            else:
                QtGui.QMessageBox.critical(self, "Error", "The movement destination must be a Description Scheme.") 
                return False

    # ### Context Menu ###
    def conceptTreeContextMenu(self, position):
        if isinstance(self.selectedDItems[0], DescriptionScheme):
            menu = QtGui.QMenu()
            menu.addAction(self.tr("Add new Description Scheme"))
            menu.actions()[-1].triggered.connect(self.contextMenuAddDescriptionScheme)
            menu.addAction(self.tr("Add new Descriptor"))
            menu.actions()[-1].triggered.connect(self.contextMenuAddDescriptor)
            menu.addSeparator()
            menu.addAction(self.tr("Rename"))
            menu.actions()[-1].triggered.connect(self.contextMenuRename)
            menu.addAction(self.tr("Move"))
            menu.actions()[-1].triggered.connect(self.contextMenuMove)
            menu.addAction(self.tr("Delete"))
            menu.actions()[-1].triggered.connect(self.contextMenuDelete)
#             menu.addSeparator()
#             menu.addAction(self.tr("Settings"))
#             menu.actions()[-1].triggered.connect(self.contextMenuConceptSettings)
            
            menu.exec_(self.viewport().mapToGlobal(position))
        
        if isinstance(self.selectedDItems[0], Descriptor):
            menu = QtGui.QMenu()
            menu.addAction(self.tr("Move"))
            menu.actions()[-1].triggered.connect(self.contextMenuMove)
            menu.addAction(self.tr("Delete"))
            menu.actions()[-1].triggered.connect(self.contextMenuDelete)
#             menu.addSeparator()
#             menu.addAction(self.tr("Settings"))
#             menu.actions()[-1].triggered.connect(self.contextMenuDescriptorSettings)
            
            menu.exec_(self.viewport().mapToGlobal(position))
    
    def contextMenuRename(self):
        for dItem in self.selectedDItems:
            if isinstance(dItem, DescriptionScheme):
                repeatInput = True
                while repeatInput:
                    text, qInpReturn = QtGui.QInputDialog.getText(self, 'Rename', 'Enter new name:', text=dItem.name)
                    if qInpReturn:
                        if dItem.rename(str(text)):
                            treeObj = self.selectedItems()
                            treeObj[0].setText(0,text)
                            repeatInput = False
                        else:
                            QtGui.QMessageBox.critical(self, "Error", "Name can not be empty.")
                            repeatInput = True
                    else:
                        repeatInput = False
    
    def contextMenuMove(self):
        QtGui.QMessageBox.information(self, "Information", "Use drag and drop for moving Objects.")
    
    def contextMenuAddDescriptor(self):
        parent = self.selectedDItems[0]
        classes = Descriptor.__subclasses__()
        for oneClass in classes:
            if not hasattr(oneClass, 'initViaGui'):
                classes.remove(oneClass)
        
        items = list()
        itemDict = dict()
        for oneClass in classes:
            name = str(oneClass.__name__)
            items.append(name)
            itemDict[name] = oneClass
        item, ok = QtGui.QInputDialog.getItem (self, "Select Descriptor", "Select the Descriptor.", items, current = 0, editable = False)
        if ok:
            SelectedDescriptor = itemDict.get(str(item));
            newDescriptor = SelectedDescriptor('User')
            newDescriptor.initViaGui(self.vd.mainWin.ui.filmView);
            parent.addDescriptor(newDescriptor)
            self.createObjectTree()
    
    def contextMenuAddDescriptionScheme(self):
        dItem = self.selectedDItems[0]
        
        repeatInput = True
        
        while repeatInput:
            text, qInpReturn = QtGui.QInputDialog.getText(self, 'Add new Description Scheme', 'Enter name of new Description Scheme:', text='New Item')
            
            if qInpReturn and len(text) > 0:
                newSemObj = DescriptionScheme(str(text), 'User')
                dItem.addDescriptionScheme(newSemObj)
                self.createObjectTree();
                repeatInput = False
            elif qInpReturn:
                repeatInput = True
            else:
                repeatInput = False
    
    def contextMenuDelete(self):
        # TODO: delete recursive or add children to parent node or not allowed? 
        semObj = self.selectedDItems[0]
        
        if not semObj is None:
            ret = QtGui.QMessageBox.question(self, 'Delete', 'Are you sure to delete this Object?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if ret == QtGui.QMessageBox.Yes:
                semObj.delete()
            
        treeObj = self.selectedItems()
        if len(treeObj):
            treeObj[0].parent().removeChild(treeObj[0])
    
    def contextMenuConceptSettings(self):
        pass
    
    # ### Show functions ###
    def createObjectTree(self):
        dsRoot = self.vd.data.dsRoot
        if dsRoot is None:
            return
        
        self.clear()
        
        stringList = QtCore.QStringList(QtCore.QString(dsRoot.name))
        uiItem = QtGui.QTreeWidgetItem(stringList)
        self.itemDict[uiItem] = dsRoot
        self.insertTopLevelItem(0,uiItem)
        
        self.createObjectInObjectTree(dsRoot, uiItem)
        
        self.sortItems(0,0)
        self.expandAll()

    def createObjectInObjectTree(self, dsObject, uiItem):
        for i,actDescriptor in enumerate(dsObject.getDescriptors()):
            child = QtGui.QTreeWidgetItem(QtCore.QStringList(QtCore.QString(actDescriptor.getTypeString() + " (" + actDescriptor.getValueString() + ")")))
            child.setTextColor(0,QtGui.QColor(100,100,100))
            child.setFont(0,QtGui.QFont("", pointSize=9, italic=True))
            self.itemDict[child] = actDescriptor
            uiItem.insertChild(0,child)
        
        for i,actDescrScheme in enumerate(dsObject.getDescriptionSchemes()):
            child = QtGui.QTreeWidgetItem(QtCore.QStringList(QtCore.QString(actDescrScheme.name)))
            uiItem.insertChild(0,child)
            self.itemDict[child] = actDescrScheme
            self.createObjectInObjectTree(actDescrScheme, child)
