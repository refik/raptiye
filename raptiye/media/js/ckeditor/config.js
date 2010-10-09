/*
Copyright (c) 2003-2010, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function(config) {
    config.language = 'tr'
    config.width = "960px"
    config.height = "500px"
    config.resize_enabled = false
    config.toolbarStartupExpanded = false
    config.toolbar = 'Full'
    config.toolbar_Full = [
        ["Bold", "Italic", "Underline", "Strike", "Subscript", "Superscript"],
        ["NumberedList", "BulletedList", "Outdent", "Indent", "Blockquote", "CreateDiv"],
        ["JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock"],
        ["Link", "Unlink", "Image", "Table", "HorizontalRule", "Smiley", "SpecialChar"],
        ["Replace", "RemoveFormat", "-", "Source"],
        ["Format", "Font", "FontSize", "TextColor", "BGColor"]
    ]
}
