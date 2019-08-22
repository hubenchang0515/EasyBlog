/* 按Tab键时添加4个空格 */
function tab(self) 
{
    if (event.keyCode == 9) 
    {
        event.preventDefault();
        var indent = '    ';
        var start = self.selectionStart;
        var end = self.selectionEnd;
        var selected = window.getSelection().toString();
        selected = indent + selected.replace(/\n/g, '\n' + indent);
        self.value = self.value.substring(0, start) + selected + self.value.substring(end);
        self.setSelectionRange(start + indent.length, start + selected.length);
    }
}