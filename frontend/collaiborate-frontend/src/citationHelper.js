import Cite from "citation-js";

export function addCitations(citations) {

    citations.forEach(citation => {
        let cit = new Cite(citation.doi)

        let output = cit.format('bibliography', {
            format: 'html',
            template: 'apa',
            lang: 'en-US'
        })

        document.getElementById(citation.id).innerHTML = output;
    })

}


