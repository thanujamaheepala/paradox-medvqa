import React, {Fragment, useEffect, useState } from 'react'
import axios from 'axios';
import Header from './components/Header'
import { ThreeDots } from  'react-loader-spinner'
import { interpolateRdYlGn } from "d3-scale-chromatic"
import colorsPic from "./colors.png";


function App() {
  const [selectedFile, setSelectedFile] = useState()
    const [preview, setPreview] = useState()
    const [isUploaded, setIsUploaded] = useState(false)
    const [data, setData] = useState([
   
    ])
    const [devData, setDevData] = useState([
   
    ])
    const [isDevView, setIsDevView] = useState(false)

    // create a preview as a side effect, whenever selected file is changed
    useEffect(() => {
        if (!selectedFile) {
            setPreview(undefined)
            return
        }

        const objectUrl = URL.createObjectURL(selectedFile)
        setPreview(objectUrl)

        // free memory when ever this component is unmounted
        return () => URL.revokeObjectURL(objectUrl)
    }, [selectedFile])

    const onSelectFile = e => {
        if (!e.target.files || e.target.files.length === 0 || !(e.target.files[0]['type'].split('/')[0] === 'image')) {
            setSelectedFile(undefined)
            return
        }
        setIsUploaded(false)
        setData([])
        setDevData([])
        // I've kept this example simple by using the first image instead of multiple
        setSelectedFile(e.target.files[0])
    }

    const handleUpload = () => {
        if (selectedFile) {
            const formData = new FormData()

		    formData.append('file', selectedFile)
            formData.append('filename', selectedFile.name)
            let url = "http://localhost:5000/upload";
            // if(isDevView){
            //   url = "http://localhost:5000/uploadDev";
            // }
            

            axios.post(url, formData, { // receive two parameter endpoint url ,form data 
            })
            .then(res => { // then print response status
                console.warn(res);
                setIsUploaded(true)
                setDevData(res.data.devData)
                // if(isDevView){
                //   setDevData(res.data.devData)
                // }
            }).catch(error => {
                console.error('There was an error!', error);
                setIsUploaded(false)
            });
        }	
	}
    const handleChange = () => {
        setIsUploaded(false)
  }
  const handleChangeDevView = () => {
    if(isDevView){
      setIsDevView(false)
    }else{
      setIsDevView(true)
    }
    
  }
  

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
          formData.append('filename', selectedFile.name)

          let url = "http://localhost:5000/predict";

          axios.post(url, formData, { // receive two parameter endpoint url ,form data 
          })
          .then(res => { // then print response status
              const newData = [{ q: filteredQ.concat("?"),a: res.data.answer,s: res.data.score}].concat(prevData)
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
    <app>
      <div className="row mt-4 text-center">
        <div className="col-md-4 offset-md-4">
          <Header/>
        </div>
        <div className="col-sm-1 offset-sm-2">
          <div className="form-check form-switch">
            <input className="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" onChange={handleChangeDevView} defaultChecked={isDevView}/>
            <label className="form-check-label" htmlFor="flexSwitchCheckDefault">Developer View</label>
          </div>
        </div>
      </div>


      {isDevView &&
        <div className="row mt-4 text-center ">
        <div className="col-md-4 offset-md-1">
          <Fragment>
              <div><label className="form-label" htmlFor="customFile">Image</label>
              <input type="file" accept=".jpg,.jpeg,.png" className="form-control rounded border border-dark" id="file" onChange={onSelectFile}/>
              {!isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" onClick={handleUpload}>Upload</button> }
              {isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" disabled onClick={handleUpload}>Upload</button> }
              </div>
              {(selectedFile && isUploaded) &&  <img src={preview} className="img-fluid rounded border border-dark mt-4" alt="Responsive image" /> }
          </Fragment>
        </div>
        <div className="col-md-3">
          <Fragment>          
          <div>
              <label className="form-label">Data</label>
          </div>
          {(devData.length==0) ? (
            <div className="rounded border border-dark mt-8 overflow-auto" style={{height: "67vh"}} >
              <div className="mb-4 mt-2 mr-1"  >
                <p style={{paddingLeft: "10px",paddingRight: "5px", textAlign: "left"}}>No Data Available</p>
              </div>
            </div>   
          ) : (
            <div className="rounded border border-dark mt-8 overflow-auto" style={{height: "67vh"}} >
              {devData.map((datum, index) => (
                <div className="mb-4 mt-2 mr-1"  key={index}>
                  <h6 style={{paddingLeft: "10px",paddingRight: "5px", textAlign: "left"}}>Q: {datum.q}</h6>
                  {!datum.a===false && 
                    <div style={{display: "flex", gap: ".5rem"}}>
                      <p style={{paddingLeft: "10px" ,paddingRight: "5px", textAlign: "left"}}>A: {datum.a}</p>
                    </div>   
                  }
                </div>
              ))}
            </div>
          )}
          
          </Fragment>
        </div>
        <div className="col-md-3">
        <Fragment>
              <div>
              <label className="form-label" htmlFor="question">Question</label>
              <input type="text" className="form-control rounded border border-dark" id="question" disabled = {(!isUploaded)? "disabled" : ""} />
              <button type="button" className="btn btn-dark btn-block mt-2" onClick={onSubmit} disabled = {(!isUploaded)? "disabled" : ""}>Submit</button>
              </div>
              {(data.length===0) ? (
                  <div></div>
              ) : (
              <Fragment>
              <div className="rounded border border-dark mt-4 overflow-auto" style={{height: "45vh"}} >
              {data.map((datum, index) => (
              <div className="mb-4 mt-2 mr-1"  key={index}>
                  <h6 style={{paddingLeft: "10px",paddingRight: "5px", textAlign: "left"}}>Q: {datum.q}</h6>
                  {datum.a===false && 
                  <ThreeDots color="#00BFFF" height={20} width={100} />}
                  {/* {!datum.a===false &&   <p style={{paddingLeft: "30px", textAlign: "left", WebkitTextStroke:"1px "+String(interpolateRdYlGn(parseFloat(datum.s)))}}>A: {datum.a+" -> "+datum.s}</p> } */}
                  {!datum.a===false && 
                  <div style={{display: "flex", gap: ".5rem"}}>
                    <p style={{paddingLeft: "5px", paddingRight: "5px", textAlign: "left", backgroundColor:String(interpolateRdYlGn(parseFloat(datum.s)))}}></p>
                    <p style={{paddingLeft: "5px" ,paddingRight: "5px", textAlign: "left"}}>A: {datum.a}</p>
                  </div>   
                  }
              </div>
              ))}
              </div>
              <img src={colorsPic} width="100%" height="10" alt="RdYlGn" style={{maxWidth: "100%"}}/>   
              <div style={{display: "flex", justifyContent: "space-between"}}>
                <span>Low-Confidence</span> 
                <span>High-Confidence</span>  
              </div>        
              </Fragment>
              )}
              
          </Fragment>
        </div>
      </div>
      }


      {!isDevView &&
        <div className="row mt-4 text-center ">
        <div className="col-md-4 offset-md-2">
          <Fragment>
              <div><label className="form-label" htmlFor="customFile">Image</label>
              <input type="file" accept=".jpg,.jpeg,.png" className="form-control rounded border border-dark" id="file" onChange={onSelectFile}/>
              {!isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" onClick={handleUpload}>Upload</button> }
              {isUploaded &&   <button type="button" className="btn btn-dark btn-block mt-2" disabled onClick={handleUpload}>Upload</button> }
              </div>
              {(selectedFile && isUploaded) &&  <img src={preview} className="img-fluid rounded border border-dark mt-4" alt="Responsive image" /> }
          </Fragment>
        </div>
        <div className="col-md-4 offset-md-0">
          <Fragment>
              <div>
              <label className="form-label" htmlFor="question">Question</label>
              <input type="text" className="form-control rounded border border-dark" id="question" disabled = {(!isUploaded)? "disabled" : ""} />
              <button type="button" className="btn btn-dark btn-block mt-2" onClick={onSubmit} disabled = {(!isUploaded)? "disabled" : ""}>Submit</button>
              </div>
              {(data.length===0) ? (
                  <div></div>
              ) : (
              <Fragment>
              <div className="rounded border border-dark mt-4 overflow-auto" style={{height: "45vh"}} >
              {data.map((datum, index) => (
              <div className="mb-4 mt-2 mr-1"  key={index}>
                  <h6 style={{paddingLeft: "10px",paddingRight: "5px", textAlign: "left"}}>Q: {datum.q}</h6>
                  {datum.a===false && 
                  <ThreeDots color="#00BFFF" height={20} width={100} />}
                  {/* {!datum.a===false &&   <p style={{paddingLeft: "30px", textAlign: "left", WebkitTextStroke:"1px "+String(interpolateRdYlGn(parseFloat(datum.s)))}}>A: {datum.a+" -> "+datum.s}</p> } */}
                  {!datum.a===false && 
                  <div style={{display: "flex", gap: ".5rem"}}>
                    <p style={{paddingLeft: "5px", paddingRight: "5px", textAlign: "left", backgroundColor:String(interpolateRdYlGn(parseFloat(datum.s)))}}></p>
                    <p style={{paddingLeft: "5px" ,paddingRight: "5px", textAlign: "left"}}>A: {datum.a}</p>
                  </div>   
                  }
              </div>
              ))}
              </div>
              <img src={colorsPic} width="100%" height="10" alt="RdYlGn" style={{maxWidth: "100%"}}/>   
              <div style={{display: "flex", justifyContent: "space-between"}}>
                <span>Low-Confidence</span> 
                <span>High-Confidence</span>  
              </div>        
              </Fragment>
              )}
              
          </Fragment>
        </div>
      </div>
      }
    </app>   
  )
}


export default App;
