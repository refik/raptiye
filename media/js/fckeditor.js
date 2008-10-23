// raptiye
// Copyright (C)  Alper KANAT  <alperkanat@raptiye.org>
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

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