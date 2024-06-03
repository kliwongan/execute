"use client";
import React, { useState, useRef } from "react";
import CodeEditorWindow from "./CodeEditorWindow";
import Button from "./Button";

const API_URL: string = "http://127.0.0.1:8000";

export default function Home() {
  const [val, setVal] = useState("");
  const myDivRef = useRef();

  const onTestCode = () => {
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: val }),
    };
    fetch(API_URL + "/test_code", options)
      .then((response) => response.json())
      .then((data) => {
        console.log("Incoming request: " + JSON.stringify(data));
        if (data != undefined && data.output != undefined) {
          myDivRef.current.value = data.output;
        } else if (data != undefined && data.detail != undefined) {
          myDivRef.current.value = data.detail;
        }
      })
      .catch((error) => {
        console.error("Error: " + error);
        if (data != undefined && data.output != undefined) {
          myDivRef.current.value = data.detail;
        }
      });
  };

  const onSubmitCode = () => {
    const options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: val }),
    };
    fetch(API_URL + "/submit_code", options)
      .then((response) => response.json())
      .then((data) => {
        console.log("Incoming request: " + JSON.stringify(data));
        if (data != undefined && data.output != undefined) {
          myDivRef.current.value = data.output;
        } else if (data != undefined && data.detail != undefined) {
          myDivRef.current.value = data.detail;
        }
      })
      .catch((error) => {
        console.error("Error: " + error);
        if (data != undefined && data.output != undefined) {
          myDivRef.current.value = data.detail;
        }
      });
  };

  const onCodeUpdate = (value: string) => {
    setVal(value);
    console.log(value);
  };

  return (
    <>
      <div className="grid grid-cols-2 gap-2">
        <div>
          <CodeEditorWindow
            language={"python3"}
            theme={"vs-dark"}
            onChange={onCodeUpdate}
          ></CodeEditorWindow>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Button text={"Test Code"} onClick={onTestCode}></Button>
            </div>
            <div>
              <Button text={"Submit Code"} onClick={onSubmitCode}></Button>
            </div>
          </div>
        </div>
        <div>
          <textarea
            ref={myDivRef}
            id="code_output"
            className="block p-2.5 w-full h-full text-sm text-white bg-black rounded-lg border"
            placeholder="Code output"
          ></textarea>
        </div>
      </div>
    </>
  );
}
