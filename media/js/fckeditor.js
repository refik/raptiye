FCKConfig.AutoDetectLanguage = false;
FCKConfig.DefaultLanguage = "tr";
FCKConfig.StartupFocus = true;
FCKConfig.StartupShowBlocks = true;
FCKConfig.DefaultLinkTarget = '_blank';
FCKConfig.BaseHref = 'http://raptiye.org/';
FCKConfig.EnterMode = "br";
FCKConfig.ShiftEnterMode = "br";
FCKConfig.TabSpaces = 4;
FCKConfig.ShowBorders = true;
FCKConfig.ToolbarSets["Default"] = [
	['Source','DocProps','Preview'],
	['Cut','Copy','Paste','PasteText','PasteWord','-'],
	['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
	['FitWindow','ShowBlocks','-','About'],
	'/',
	['Table','TableInsertRowAfter','TableDeleteRows','TableInsertColumnAfter'],
	['TableDeleteColumns','TableInsertCellAfter','TableDeleteCells'],
	['TableMergeCells', 'TableHorizontalSplitCell','TableCellProp'],
	'/',
	['Bold','Italic','Underline','StrikeThrough','-','Subscript','Superscript'],
	['OrderedList','UnorderedList','-','Outdent','Indent','Blockquote'],
	['JustifyLeft','JustifyCenter','JustifyRight','JustifyFull'],
	['Link','Unlink','Anchor'],
	['Image','Flash','Rule','SpecialChar'],
	'/',
	['Style','FontFormat','FontName','FontSize'],
	['TextColor','BGColor']
];
FCKConfig.SkinPath = FCKConfig.BasePath + 'skins/silver/';
FCKConfig.Plugins.Add("tablecommands")
FCKConfig.Plugins.Add("dragresizetable")