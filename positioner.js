var positionedElements;
var positionedElementsIterator = 0;
$(document).ready( function () {
	var windowWidth = $(window).width();
	var windowHeight = $(window).height();

	positionedElements = new Array($('div').length);

	$('div').each( function() {
		originalWidth = $(this).width()
		while ($(this).position().left + originalWidth > windowWidth ||$(this).position().left < 0) {
			$(this).css('left', Math.random() * windowWidth);
		}
		var top = $(this).position().top
		var left = $(this).position().left
		positionedElements[positionedElementsIterator++] = [top, left, top + $(this).height(), left + $(this).width()]

		var i = 0;
		while (i != positionedElementsIterator - 1) {
			i++;
		}
	});
});