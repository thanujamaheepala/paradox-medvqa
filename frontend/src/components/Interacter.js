import React, {Fragment, useEffect, useState } from 'react'
import { ThreeDots } from  'react-loader-spinner'
import axios from 'axios';

const Interacter = () => {
    const [data, setData] = useState([
   
    ])

    const onSubmit = e => {
        const q = document.getElementById("question").value
        const filteredQ = q.replace(/[^a-zA-Z0-9 ]/g, '');
        const prevData = data
        if(filteredQ.length !== 0){
            const newData = [{ q: filteredQ.concat("?"),a: false}].concat(prevData)
            setData(newData)
            document.getElementById("question").value = ""

            const formData = new FormData()

		    formData.append('question',filteredQ)
            let url = "http://localhost:5000/predict";

            axios.post(url, formData, { // receive two parameter endpoint url ,form data 
            })
            .then(res => { // then print response status
                const newData = [{ q: filteredQ.concat("?"),a: res.data}].concat(prevData)
                setData(newData)
                console.log(res)
            }).catch(error => {
                console.error('There was an error!', error);
                var newData = data
                newData.pop(0)
                setData(newData)
            });
        }   
    }

    return (
        <Fragment>
            <div>
            <label className="form-label" htmlFor="question">Question</label>
            <input type="text" className="form-control rounded border border-dark" id="question" />
            <button type="button" className="btn btn-dark btn-block mt-2" onClick={onSubmit}>Submit</button>
            </div>
            {(data.length===0) ? (
                <div></div>
            ) : (
                <div className="rounded border border-dark mt-4" style={{height: "45vh"}} >
            {data.map((datum, index) => (
            <div className="mb-4 mt-2 mr-1"  key={index}>
                <h6 style={{paddingLeft: "10px", textAlign: "left"}}>Q: {datum.q}</h6>
                {datum.a===false && <ThreeDots color="#00BFFF" height={20} width={100} />}
                {!datum.a===false &&   <p style={{paddingLeft: "30px", textAlign: "left"}}>A: {datum.a}</p> }
            </div>
            ))}
            </div>
            )}
            
        </Fragment>
    )
}

export default Interacter
