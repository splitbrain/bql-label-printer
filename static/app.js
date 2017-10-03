const labelSelect = document.getElementById('sel-label');
const wrapper = document.getElementById('wrapper');
const form = document.getElementById('form');
const button = document.getElementById('btn');

/**
 * Load a template
 */
labelSelect.onchange = function loadTemplate() {
    fetch('/static/labels/' + labelSelect.value + '.html')
        .then(function (response) {
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok.');
        })
        .then(function (text) {
            wrapper.innerHTML = text;
            buildForm();
        })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
            alert(error)
        })
    ;
};
labelSelect.onchange(); // first load

/**
 * Create the input form for the loaded template
 */
function buildForm() {
    const inputs = wrapper.querySelectorAll('.input');
    form.innerHTML = '';

    for (let input of inputs) {

        let inp = document.createElement('textarea');
        inp.placeholder = input.innerText;
        inp.oninput = function () {
            input.innerText = inp.value;
        };

        form.appendChild(inp);
    }
}

/**
 * Return the currently used label size
 *
 * @return {string}
 */
function getSize() {
    return labelSelect.value.split('_')[0];
}

/**
 * Print the label
 */
button.onclick = function () {
    //const node = document.getElementById('label');
    const node = wrapper.querySelector(':first-child');

    domtoimage.toBlob(node)
        .then(function (blob) {
            const fd = new FormData();
            fd.append('data', blob);
            fd.append('size', getSize());

            return fetch('/print', {
                method: 'POST',
                body: fd
            });
        })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('Printing failed');
            }
        })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
            alert(error)
        })
    ;

    /*
    domtoimage.toPng(node)
        .then(function (dataUrl) {
            var img = new Image();
            img.src = dataUrl;
            document.body.appendChild(img);
        })
        .catch(function (error) {
            console.error('oops, something went wrong!', error);
        });
     */
};

