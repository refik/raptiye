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

window.onload = function() {
	if (document.getElementById("id_content") != null) {
		// for content of frontpage
		var content_editor = new FCKeditor('id_content')
		content_editor.BasePath = "/media/js/fckeditor/"
		content_editor.Width = "750px"
		content_editor.Height = "300px"
		content_editor.ReplaceTextarea()
	}
	
	if (document.getElementById("id_footer") != null) {
		// for footer
		var footer_editor = new FCKeditor('id_footer')
		footer_editor.BasePath = "/media/js/fckeditor/"
		footer_editor.Width = "750px"
		footer_editor.Height = "300px"
		footer_editor.ReplaceTextarea()
	}
}