"use client"

import { AuthDialog } from "@/components/envconverter/AuthDialog";
import { GlowingAboutIcon } from "@/components/GlowingAbout";
import { GlowingGithubIcon } from "@/components/GlowingGithub";
import { GlowingHomeIcon } from "@/components/GlowingHome";
import { GlowingServicesIcon } from "@/components/GlowingService";
import { Button } from "@/components/ui/button";
import { FileText } from "lucide-react";
import { useState } from "react";



export default function Home() {

  const [dialogOpen, setDialogOpen] = useState(false);
  // bg-gradient-to-br from-purple-600 to-blue-700 - the css gradient


  return (
    <>
    <div className="bg-gradient-to-br from-yellow-600 to-white">
      <header className="flex justify-center items-center p-5 ">
        <div className="flex items-center space-x-10 bg-white/10 backdrop-blur-md rounded-full px-10 py-4 shadow-lg">
          <GlowingHomeIcon />
          <GlowingAboutIcon />
          <GlowingServicesIcon />
          <GlowingGithubIcon />
        </div>
      </header>

      <main className="min-h-[calc(100vh-88px)] flex items-center justify-center">
        <div className="text-center space-y-8 p-6">
          <div className="space-y-4">
            <h1 className="text-4xl font-bold tracking-tighter text-white">
              Automate your Job Applications
            </h1>
            <p className="text-xl text-white/80">
              Currently works on Naukri.com
            </p>
          </div>
          
          <Button
            size="lg"
            className="text-lg px-8 py-6 rounded-full shadow-lg hover:shadow-xl transition-all duration-300"
            onClick={() => setDialogOpen(true)}
          >
            <FileText className="mr-2 h-6 w-6" />
            ENV Variables
          </Button>

          <AuthDialog open={dialogOpen} onOpenChange={setDialogOpen} />
        </div>
      </main>
      </div>
    </>
  );
}
