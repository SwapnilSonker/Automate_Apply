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

  const handleApiCall = async () => {
    setIsLoading(true);
    try {
      // Simulating API call with timeout
      await new Promise(resolve => setTimeout(resolve, 1500));
      const jsonData = parseEnvToJson(envInput);
      setApiResponse(jsonData);
    } catch (error) {
      console.error('API call failed:', error);
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
              <Button 
                className="flex-1"
                onClick={handleDownloadCsv}
                variant="secondary"
              >
                <Download className="mr-2 h-4 w-4" />
                Download CSV
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}