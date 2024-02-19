window.addEventListener('load', (e) => {
    const btns = document.getElementsByClassName('add-settings-value');

    for (let btn of btns) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.currentTarget.classList.add('hidden');
            e.currentTarget.previousSibling.previousSibling.classList.remove('hidden');
        });
    }
});