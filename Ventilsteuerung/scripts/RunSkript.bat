::Script

@echo off & setlocal

del ..\4diacIDE-workspace\test\FBs\Counter\const\DefaultPool.gcf
del ..\4diacIDE-workspace\test\FBs\Counter\const\DefaultPool_Numeric.gcf
python GcfScript.py --oldfile ISO-DesignerProjects\Workspace\DefaultPool\Output\DefaultPool.iop.h --newfolder 4diacIDE-workspace\test\FBs\Counter\const\ --newfile DefaultPool --package FBs::Counter::const --jopfile ISO-DesignerProjects\Workspace\DefaultPool\DefaultPool.jop
