import React, { Component } from 'react'

class Assessment extends Component {
    constructor(props) {
        super(props);
    
         this.state = {
           boolean_question: {},
           mcq:{}
        };
    
        this.gen_questions = this.gen_questions.bind(this);
        this.onSubmit=this.onSubmit.bind(this);
      }
      componentDidMount() {
        this.gen_questions();
     }
    
      gen_questions(){
        // ev.preventDefault();
        fetch('http://localhost:5000/assessments', {
      method: 'POST',
      body:JSON.stringify({'data':this.props.location.data}),
      headers: new Headers({
        "content-type": "application/json"
      }),
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ boolean_question: body.bool, mcq:body.mcq});
        console.log(this.state);
        // document.getElementById("text").innerHTML=body.text;
        // document.getElementById("summary").innerHTML=body.summary;
        // document.getElementsByClassName("heading")[0].style.visibility="visible";
        // document.getElementsByClassName("container1")[0].style.visibility="visible";
        // document.getElementsByClassName("heading")[0].style.display="flex";
        // document.getElementsByClassName("container1")[0].style.display="flex";
      });
    });
  }
  onSubmit(e) {
    e.preventDefault()
    // var formElements = 
    console.log(this.state.mcq.length);
    var s=0;
    for(var i=0;i<Object.keys(this.state.mcq).length;i++){
      // var ans=document.getElementsByName(i.toString())
      // if(ans.checked)
      this.state.mcq[i]["user_answer"]=document.querySelector("input[name=\'"+i.toString()+"\']:checked").value;
      // ans.value;
      if(this.state.mcq[i]["user_answer"]===this.state.mcq[i]["answer"])
        s+=1;
    }

    console.log(this.state.mcq);
    console.log(s);
    document.getElementById("score").innerHTML="Your score is : "+s+"/"+Object.keys(this.state.mcq).length;
  }

  render() {
    //   this.gen_questions()
    return (
    // <form noValidate onSubmit={this.onSubmit}>
    <div>
      <form noValidate onSubmit={this.onSubmit} name="qa">
      {
        Object.keys(this.state.mcq).map((key, index) => ( 
            <div className="jumbotron mt-5" key={index}>
           <div className="col-sm-8 mx-auto">
          <h3 className="text-body">{index+1}) {this.state.mcq[key]["question_statement"]}</h3> 

          {
          this.state.mcq[key]["options"].map((option,index1) => (
            <div style={{color: 'black', textAlign: 'left', fontSize:'2vh' }}>
              <input type="radio" name={index} value={option}/>  {option}
            </div>)
          )}
          </div>
          </div>
        ))
      }
    <input type="submit" className="btn-secondary btn-lg"/>
    </form>
    <hr></hr>
    <div id="score" style={{color: 'white', textAlign: 'center', fontSize:'4vh' }}></div>
    </div>
    )
  }
}

export default Assessment