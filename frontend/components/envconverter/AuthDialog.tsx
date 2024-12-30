"use client";

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Rocket, Download } from "lucide-react";
import { useState } from "react";
import { EnvInput } from "./EnvInput";
import { downloadCsv, parseEnvToJson, convertToCsv } from "@/lib/csv-utils";

interface AuthDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AuthDialog({ open, onOpenChange }: AuthDialogProps) {
  const [envInput, setEnvInput] = useState("");
  const [apiResponse, setApiResponse] = useState<Record<string, string> | null>(null);
  const [isLoading, setIsLoading] = useState(false);


  const parseEnvInput = (input: string) => {
    const envObject: Record<string, string> = {};
  
    // Split input by lines, trim spaces, and ignore empty lines
    const lines = input.split('\n')
      .map(line => line.trim())         // Trim spaces around each line
      .filter(line => line.length > 0); // Remove empty lines
  
    // Regex to match key-value pairs, either : or = as separator
    const regex = /^([A-Za-z_][A-Za-z0-9_]*)\s*[:=]\s*"(.*?)"$/;
  
    console.log("Processing input: ", lines);
  
    // Process each line
    lines.forEach((line, index) => {
      // Remove trailing comma if it exists
      const lineWithoutComma = line.replace(/,\s*$/, '');
  
      console.log(`Processing line ${index + 1}:`, lineWithoutComma); // Log each line to check
  
      const match = lineWithoutComma.match(regex);
  
      if (match) {
        const [, key, value] = match; // Destructure to get key and value
        console.log(`Matched key: ${key}, value: ${value}`); // Log matched key-value pair
        envObject[key] = value; // Add to the envObject
      } else {
        console.warn(`Line ${index + 1} did not match regex:`, lineWithoutComma); // Log unmatched lines
      }
    });
  
    return envObject;
  };



  const handleApiCall = async () => {
    setIsLoading(true);
    console.log("inner input" , envInput)
    const env = parseEnvInput(envInput);
    console.log("env input", env);
    const stringified = JSON.stringify(env)
    console.log("string" , stringified)
    try {
      // Simulating API call with timeout
      // const response = await fetch("http://127.0.0.1:5000/start", {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json'
      //   },
      //   body : JSON.stringify(env)
      // });
      
      // if(response.ok){
      //   const jsonData = await response.json();

      //   setApiResponse(jsonData)
      // }
      // else{
      //   console.log("API call failed" , response.statusText);
      //   setApiResponse({error: "API call failed", details: response.statusText});
      // }


    } catch (error) {
      console.error('API call failed:', error);
      // setApiResponse({error: 'Network error', details: error.message})
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadCsv = () => {
    if (!apiResponse) return;
    const csvContent = convertToCsv(apiResponse);
    downloadCsv(csvContent, 'environment-variables.csv');
  };


  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Convert Environment Variables</DialogTitle>
        </DialogHeader>
        <div className="space-y-6 py-4">
          <EnvInput value={envInput} onChange={setEnvInput} />

          <div className="flex gap-4">
            <Button 
              className="flex-1"
              onClick={handleApiCall}
              disabled={!envInput.trim() || isLoading}
            >
              <Rocket className="mr-2 h-4 w-4" />
              {isLoading ? "Processing..." : "Fire Apply"}
            </Button>
            {apiResponse && (
                <>
                <div className="flex-1">
                {/* <pre className="bg-gray-100 p-2 rounded">{JSON.stringify(apiResponse, null, 2)}</pre> */}
                <Button
                className="mt-2 w-full"
                onClick={handleDownloadCsv}
                variant="secondary"
                >
                <Download className="mr-2 h-4 w-4" />
                {JSON.stringify(apiResponse["applied_jobs"], null, 2)}
                </Button>
                </div>
                </>
              )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}