$(document).ready(function() {
  "use strict"; // Start of use strict
	let files;
	
	const b64toBlob = (b64Data, contentType = '', sliceSize = 512) => {
		const byteCharacters = atob(b64Data);
		const byteArrays = [];
	  
		for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
		  const slice = byteCharacters.slice(offset, offset + sliceSize);
	  
		  const byteNumbers = new Array(slice.length);
		  for (let i = 0; i < slice.length; i++) {
			byteNumbers[i] = slice.charCodeAt(i);
		  }
	  
		  const byteArray = new Uint8Array(byteNumbers);
		  byteArrays.push(byteArray);
		}

	return new Blob(byteArrays, {type: contentType});
	}

	const onUploadError = (jqxhr, status, errorMessage) => {
		$('#loadingBtn').attr('hidden', true);

		console.log('On Upload Error', errorMessage);
	}

	const onUploadSuccess = (response, status, jqxhr) => {

		$('#uploadBtn').attr('hidden', false);

		//$('.loader').invisible();
		$('#portfolio-container').visible();

		//Enable the download section if the response contains actual results
		if(Object.keys(response.results).length > 0){
			$('#download').show();
			$('#loadingBtn').attr('hidden', true);
			$('#uploadBtn').attr('hidden', false);
		}

		let row = $('#portfolio-container').find('.row')[0];
		$(row).empty();

		//Fill the portfolio-templates with images and related data
		Object.keys(response.results).forEach(key => {

			//Convert base64 string image into Blob
			let blob = b64toBlob(response.results[key], 'image/jpeg');
			//Creates the URL
			const url = URL.createObjectURL(blob);

			let portfolioTemplate = $('#hidden-portfolio-template').html();
			let portfolio = $(portfolioTemplate)[0];

			let image = $(portfolio).find('img')[0];			
			$(image).attr('src', `data:image/jpeg;base64, ${response.results[key]}`);
			
			let anchor = $(portfolio).find("a")[0];
			$(anchor).attr('href', url);

			let text = $(portfolio).find(".project-category")[0];
			$(text).text(key);

			console.log('portfolio', portfolio)

			$(row).append(portfolio);
		});

		//Attach the batchId to the download button
		let downloadSection = $('#download');

		let button = $(downloadSection).find("a")[0];

		$(button).click((event) => {
			event.preventDefault();

			let params = {
				'fileName': 'results'
			};

			downloadFile(response.uuid, onDownloadSuccess, onDownloadError, params);
		});
	}

	const onDownloadError = (jqxhr, status, errorMessage) => {
		$('#loadingBtn').attr('hidden', true);
		console.log('On Download Error', errorMessage);
	}

	const onDownloadSuccess = (response, status, jqxhr, params) => {
		if (navigator.appVersion.toString().indexOf('.NET') > 0) {
            window.navigator.msSaveOrOpenBlob(response, params['fileName']);
        }

        // FireFox
        else if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1) {
            // Do Firefox-related activities
            var link = document.createElement('a');
            // Add the element to the DOM
            link.setAttribute("type", "hidden"); // make it hidden if needed
            link.download = params['fileName'];
            link.href = window.URL.createObjectURL(response);
            document.body.appendChild(link);
            link.click();
            link.remove();
        }

        else {
            let a = document.createElement("a");

            a.href = window.URL.createObjectURL(response)
            a.download = params['fileName'];
            a.click();
        }
	}


	const downloadFile = (batchId, onSuccess, onError, params = undefined) => {
		let request = {
			type: 'GET',
			url: `/api/download/${batchId}`,
			xhrFields:{
                responseType: 'blob'
            },
			//contentType: false,
			//processData: false,
			crossDomain: true,
			cache: false,
			success: (response, status, jqxhr) => onSuccess(response, status, jqxhr, params), //onSuccess(response, params),
			error: onError
		};
		
		$.ajax(request);
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
		console.log('Upload button clicked');

		$('#portfolio-container').show().invisible();
		$('#download').hide();

        if (files && files.length > 0) {

        	$('#uploadBtn').attr('hidden', true);
			$('#loadingBtn').attr('hidden', false);

            let file = files[0];
			let fileName = file.name.split('.')[0];
			
			let formData = new FormData();
			formData.append('file', file);
			
			let params = {
				'fileName': fileName
			};

			uploadFile(formData, onUploadSuccess, onUploadError, params);
		}
        else {
			alert("No file has been provided. Analysis shall not start");
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
			return (visibility === 'visible') ? 'hidden' : 'visible';
		});
	};
});

