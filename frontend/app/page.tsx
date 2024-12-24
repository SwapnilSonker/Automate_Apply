import { GlowingAboutIcon } from "@/components/GlowingAbout";
import { GlowingGithubIcon } from "@/components/GlowingGithub";
import { GlowingHomeIcon } from "@/components/GlowingHome";
import { GlowingServicesIcon } from "@/components/GlowingService";

export default function Home() {
  return (
    <>
      <header className="flex justify-center items-center p-5">
        <div className="flex items-center space-x-10 bg-white/10 backdrop-blur-md rounded-full px-10 py-4 shadow-lg">
          <GlowingHomeIcon />
          <GlowingAboutIcon />
          <GlowingServicesIcon />
          <GlowingGithubIcon />
        </div>
      </header>
    </>
  );
}
