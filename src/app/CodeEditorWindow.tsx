"use client";
import React, { useState } from "react";
import Editor from "@monaco-editor/react";
import { type editor } from "monaco-editor";

type onChange = (value: string) => void;

type Props = {
  language?: string;
  code?: string;
  theme?: string;
  onChange?: onChange;
};

const CodeEditorWindow: React.FC<Props> = ({
  language,
  code,
  theme,
  onChange,
}) => {
  const getCodeFromEditor = (
    value: string,
    ev: editor.IModelContentChangedEvent
  ) => {
    onChange(value);
  };

  return (
    <div className="overlay rounded-md overflow-hidden w-full h-full shadow-4xl">
      <Editor
        height="85vh"
        width={`100%`}
        language={language || "python3"}
        theme={theme}
        defaultValue="# Type your code in here!"
        onChange={getCodeFromEditor}
      />
    </div>
  );
};
export default CodeEditorWindow;
