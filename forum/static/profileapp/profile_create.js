inputText = document.getElementsByName('birthday')[0]
lastval = ''
    
inputText.addEventListener('input', function (evt) {
    text = String(this.value)
    text = text.substr(0, 10)
    inputText.value = text
    if (text.length == 2 && lastval.length == 3 || text.length == 5 && lastval.length == 6) {
        inputText.value = text.substr(0, text.length - 1)
    } else if (text.length == 2 || text.length == 5) {
        inputText.value = text + '/'
    }
    lastval = inputText.value
});