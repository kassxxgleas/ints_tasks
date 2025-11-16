//an array, defining the routes
export default[

    {
        //the part after '#' in the url (so-called fragment):
        hash:"welcome",
        ///id of the target html element:
        target:"router-view",
        //the function that returns content to be rendered to the target html element:
        getTemplate:(targetElm) =>
            document.getElementById(targetElm).innerHTML = document.getElementById("template-welcome").innerHTML

    },

    {
        hash:"main",
        target:"router-view",
        getTemplate:createHtml4Main
    },

    {
        hash:"about",
        target:"router-view",
        getTemplate:(targetElm) =>
            document.getElementById(targetElm).innerHTML = document.getElementById("template-about").innerHTML
    }

];

function createHtml4Main(targetElm, current,totalCount){

    current=parseInt(current);
    totalCount=parseInt(totalCount);
    const data4rendering={
        currPage:current,
        pageCount:totalCount
    };



    if(current>1){
        data4rendering.prevPage=current-1;
    }

    if(current<totalCount){
        data4rendering.nextPage=current+1;
    }

    document.getElementById(targetElm).innerHTML = Mustache.render(
        document.getElementById("template-main").innerHTML,
        data4rendering
        );


/*
    return `<h1>Main Content</h1>
            ${current} <br> 
            ${totalCount} <br> 
            ${JSON.stringify(data4rendering)} 
            `;
*/
}
