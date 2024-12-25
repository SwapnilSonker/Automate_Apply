"use client";

import { useState } from 'react';
import { Button } from "../ui/button";
import { EnvInput } from "./EnvInput";
import { parseEnvToJson, convertToCsv, downloadCsv } from "@/lib/csv-utils";
import { FileDown } from "lucide-react";

export function EnvConverter() {
  const [envInput, setEnvInput] = useState('');

  const handleConvert = () => {
    const jsonData = parseEnvToJson(envInput);
    const csvContent = convertToCsv(jsonData);
    downloadCsv(csvContent, 'job_data.csv');
  };

  return (
    <div className="space-y-6">
      <EnvInput value={envInput} onChange={setEnvInput} />
      <Button
        onClick={handleConvert}
        disabled={!envInput.trim()}
        className="w-full"
      >
        <FileDown className="mr-2 h-4 w-4" />
        Download CSV
      </Button>
    </div>
  );
}