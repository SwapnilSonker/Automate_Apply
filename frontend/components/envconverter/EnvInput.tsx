"use client"

import { Label } from "../ui/label";
import { Textarea } from "../ui/textarea";


interface EnvInputProps{
    value: string;
    onChange: (value: string) => void;
}

export function EnvInput({value, onChange}: EnvInputProps){
    return (
        <>
        <div className="space-y-2">
            <Label htmlFor="env-input">
                Paste your environment variables (KEY=VALUE format)
            </Label>
            <Textarea
            id="env-input"
            placeholder = "NAUKRI_MAIL=naukri-email  NAUKRI_PASSWORD= naukri-password job_location = job location search_keyword = your job keyword "
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="h-[200px] font-mono"/>
        </div>
        </>
    )
}