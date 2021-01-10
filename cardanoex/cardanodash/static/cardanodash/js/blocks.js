let blocks = document.querySelectorAll(".block-square");

blocks.forEach((block) => {
    block.style.maxWidth = `250px`;
    block.style.minWidth = `150px`;
    block.style.maxHeight = `250px`;
    block.style.minHeight = `150px`;
    block.style.height = `${block.offsetWidth}px`;
});

window.addEventListener('resize', adjustBlockSize);

function adjustBlockSize() {
    blocks.forEach((block) => {
        block.style.height = `${block.offsetWidth}px`;
    });
}