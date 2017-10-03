var button = document.getElementById('btn');

button.onclick = function () {
    var node = document.getElementById('label');

    domtoimage.toBlob(node)
        .then(function (blob) {
            const fd = new FormData();
            fd.append('data', blob);

            console.log(blob);
            console.log(fd);

            return fetch('/print', {
                method: 'POST',
                body: fd
            });
        })
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
        });

    domtoimage.toPng(node)
        .then(function (dataUrl) {
            var img = new Image();
            img.src = dataUrl;
            document.body.appendChild(img);
        })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
        });
};

