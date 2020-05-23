$('a[data-toggle="tab"]').on('shown.bs.tab', function () {
    if ('link' in this.dataset){
        console.log(this.dataset.link)
        loadData(this.dataset.link, this.href.split('#').pop());
        delete this.dataset.link;
        setTargets()
    }
});