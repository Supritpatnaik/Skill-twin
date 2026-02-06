// Footer.tsx updates
import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer className="fixed bottom-0 left-0 w-full h-screen z-0 bg-white dark:bg-[#050505] flex flex-col justify-between p-10 md:p-16">
            {/* Top Links */}
            <div className="flex justify-between items-start w-full pt-10 px-4">
                <div className="flex gap-8 text-sm font-medium">
                    <a className="text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors" href="#">Lessons</a>
                    <a className="text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors" href="#">Resources</a>
                    <a className="text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors" href="#">Blogs</a>
                </div>
                <div className="flex gap-8 text-sm font-medium">
                    <a className="text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors" href="#">Instagram</a>
                    <a className="text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors" href="#">Twitter</a>
                    <a className="text-gray-500 hover:text-black dark:text-gray-400 dark:hover:text-white transition-colors" href="#">Youtube</a>
                </div>
            </div>

            {/* Central Branding - Fixed the wrapping issue here */}
            <div className="flex-1 flex items-center justify-center overflow-hidden">
                <h2 className="massive-footer-text text-[16vw] font-black leading-none text-gray-900 dark:text-white select-none uppercase">
                    SKILL-TWIN
                </h2>
            </div>

            {/* Bottom Bar */}
            <div className="flex justify-between items-end w-full border-t border-gray-200 dark:border-gray-800 pt-8 px-4">
                <div className="flex flex-col">
                    <span className="font-bold text-xl dark:text-white">Skill-Twin</span>
                    <span className="text-sm text-gray-500">© 2026</span>
                </div>
                
                <a href="#" className="flex items-center gap-3 group">
                    <span className="text-xl font-bold dark:text-white group-hover:pr-2 transition-all">Start Now</span>
                    <span className="material-icons text-2xl dark:text-white">arrow_forward</span>
                </a>
            </div>
        </footer>
    );
};

export default Footer;