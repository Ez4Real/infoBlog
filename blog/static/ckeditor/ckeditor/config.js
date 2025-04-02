/**
 * @license Copyright (c) 2003-2022, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// https://ckeditor.com/docs/ckeditor4/latest/api/CKEDITOR_config.html

	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.toolbarGroups = [
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'forms' },
		{ name: 'tools' },
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'others' },
		'/',
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'about' }
	];

	config.contentsCss = [
        'https://fonts.googleapis.com/css2?family=Oswald&family=Bona+Nova+SC&family=Josefin+Sans&family=Libre+Baskerville&family=Prompt&family=Dosis&family=Merriweather&family=Playfair+Display&family=Raleway&family=Smooch+Sans&family=Montserrat&display=swap',
        CKEDITOR.getUrl( 'contents.css' )
    ];

	config.font_names =
        'Oswald/Oswald, sans-serif;' +
        'Bona Nova SC/Bona Nova SC;' +
        'Josefin Sans/Josefin Sans;' +
        'Libre Baskerville/Libre Baskerville;' +
        'Prompt/Prompt, sans-serif;' +
        'Dosis/Dosis, sans-serif;' +
        'Merriweather/Merriweather;' +
        'Playfair Display/Playfair Display;' +
        'Raleway/Raleway, sans-serif;' +
        'Smooch Sans/Smooch Sans, sans-serif;' +
        'Montserrat/Montserrat, sans-serif;' +
        config.font_names;
	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	config.removeButtons = 'Underline,Subscript,Superscript';

	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Simplify the dialog windows.
	config.removeDialogTabs = 'image:advanced;link:advanced';
};
