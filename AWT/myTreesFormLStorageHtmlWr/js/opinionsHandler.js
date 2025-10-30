/**
 * Class for  handling a list (an array) of visitor opinions in local storage
 * The list is filled from a form and rendered to html
 * A template literal is used to render the opinions list
 * @author Stefan Korecko (2021)
 */
export default class OpinionsHandler {

    /**
     * constructor
     * @param opinionsFormElmId - id of a form element where a new visitor opinion is entered
     * @param opinionsListElmId - id of a html element to which the list of visitor opinions is rendered
     */
    constructor(opinionsFormElmId, opinionsListElmId){ //("opnFrm","opinionsContainer")
        this.opinions = [];

        //TODO Add opinionsElm property, referencing the div with id given by the parameter opinionsListElmId
        //TODO Add opinionsFrmElm property, referencing the form with id given by the parameter opinionsFormElmId
        this.opinionsElm = document.getElementById(opinionsListElmId);
		this.opinionsFrmElm = document.getElementById("opnFrm");
    }

    /**
     * initialisation of the list of visitor opinions and form submit setup
     */
    init(){
        if (localStorage.myTreesComments) {
            this.opinions = JSON.parse(localStorage.myTreesComments);
        }

        //TODO render opinions to html
        this.opinionsElm.innerHTML = this.opinionArray2html(this.opinions);


        this.opinionsFrmElm.addEventListener("submit", event => this.processOpnFrmData(event));
    }

    /**
     * Processing of the form data with a new visitor opinion
     * @param event - event object, used to prevent normal event (form sending) processing
     */
    processOpnFrmData(event){
        //1.prevent normal event (form sending) processing
        event.preventDefault();

        //2. Read and adjust data from the form (here we remove white spaces before and after the strings)
        const nopName = this.opinionsFrmElm.elements["nameElm"].value.trim(); // this.opinionsFrmElm.elements["login"] can be used, too
        const nopOpn = this.opinionsFrmElm.elements["opnElm"].value.trim(); // this.opinionsFrmElm.elements["comment"] can be used, too
        const nopWillReturn = this.opinionsFrmElm.elements["willReturnElm"].checked;

        //3. Verify the data
        if(nopName=="" || nopOpn==""){
            window.alert("Please, enter both your name and opinion");
            return;
        }

        //3. Add the data to the array opinions and local storage
        const newOpinion =
            {
                name: nopName,
                comment: nopOpn,
                willReturn: nopWillReturn,
                created: new Date()
            };

        console.log("New opinion:\n "+JSON.stringify(newOpinion));

        this.opinions.push(newOpinion);

        localStorage.myTreesComments = JSON.stringify(this.opinions);


        //4. Update HTML
        //TODO add the new opinion to HTML
        this.opinionsElm.innerHTML+=this.opinion2html(newOpinion);



        //5. Reset the form
        this.opinionsFrmElm.reset(); //resets the form
    }

    /**
     * creates html code for one opinion using a template literal
     * @param opinion - object with the opinion
     * @returns {string} - html code with the opinion
     */
    opinion2html(opinion){
        //TODO finish opinion2html
        const opinionTemplate=
		   `<section>
			   <h3>${opinion.name} <i>(${(new Date(opinion.created)).toDateString()})</i></h3>

			   <p>${opinion.comment}</p>
			   <p>${opinion.willReturn?"I will return to this page.":"Sorry, one visit was enough."}</p>
			</section>`;
		return opinionTemplate;
    }

    /**
     * creates html code for all opinions in an array using the opinion2html method
     * @param sourceData -  an array of visitor opinions
     * @returns {string} - html code with all the opinions
     */
    opinionArray2html(sourceData){
        //TODO finish opinionArray2html
		let htmlWithOpinions="";
		for(const opn of sourceData){
			htmlWithOpinions += this.opinion2html(opn);
		}
		return htmlWithOpinions;
    }

}



