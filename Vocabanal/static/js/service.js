$(document).ready(function() {
  "use strict"; // Start of use strict
	let files;
	
	const onError = (jqxhr, status, errorMessage) => {
		$('.loader').invisible();
		
		console.log('On Error', errorMessage);
	}

	const onSuccess = (response, status, jqxhr) => {
		$('.loader').invisible();
		$('.portfolio-container').visible();
		console.log('On Success');
	}
	
    const uploadFile = (formData, onSuccess, onError, params) => {
		let request = {
			type: 'POST',
			url: '/api/upload',
			data: formData,
			contentType: false,
			processData: false,
			crossDomain: true,
			cache: false,
			success: onSuccess, //onSuccess(response, params),
			error: onError
		};
		
		$.ajax(request);
	}

	$('#fileSelect').change((event) => {
		
		console.log('File changed');
        files = event.target.files;

		event.preventDefault();
	});

	$('#uploadBtn').click((event) => {
		event.preventDefault();
		$('.loader').visible();
		$('.portfolio-container').invisible();
		console.log('Upload button clicked');

        if (files && files.length > 0) {

            let file = files[0];
			let fileName = file.name.split('.')[0];
			
			let formData = new FormData();
			formData.append('file', file);
			
			let params = {
				'fileName': fileName
			};

			uploadFile(formData, onSuccess, onError, params);
		}
	});

	jQuery.fn.visible = function() {
		return this.css('visibility', 'visible');
	};
	
	jQuery.fn.invisible = function() {
		return this.css('visibility', 'hidden');
	};
	
	jQuery.fn.visibilityToggle = function() {
		return this.css('visibility', function(i, visibility) {
			return (visibility == 'visible') ? 'hidden' : 'visible';
		});
	};
});

