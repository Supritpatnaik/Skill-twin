
import React from 'react';
import ThemeToggle from './ThemeToggle';

interface HeaderProps {
    isDarkMode: boolean;
    toggleTheme: () => void;
    onGetStartedClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ isDarkMode, toggleTheme, onGetStartedClick }) => {
    return (
        <header className="fixed top-0 w-full z-50 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-xl border-b border-gray-200 dark:border-border-dark transition-colors duration-300">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center py-4">
                    <div className="flex items-center gap-2">
                        <span className="font-extrabold text-xl tracking-tight text-gray-900 dark:text-white uppercase">Skill-Twin</span>
                    </div>
                    <nav className="hidden md:flex gap-8 text-sm font-medium items-center">
                        <a className="text-gray-600 dark:text-gray-400 hover:text-primary dark:hover:text-primary transition-colors hover:bg-gray-100 dark:hover:bg-white/5 px-3 py-2 rounded-md" href="#">How it Works</a>
                        <a className="text-gray-600 dark:text-gray-400 hover:text-primary dark:hover:text-primary transition-colors hover:bg-gray-100 dark:hover:bg-white/5 px-3 py-2 rounded-md" href="#">Impact</a>
                        <a className="text-gray-600 dark:text-gray-400 hover:text-primary dark:hover:text-primary transition-colors hover:bg-gray-100 dark:hover:bg-white/5 px-3 py-2 rounded-md" href="#">Tech Stack</a>
                    </nav>
                    <div className="flex items-center gap-4">
                        <ThemeToggle isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
                        <button 
                            onClick={onGetStartedClick}
                            className="bg-primary hover:bg-primary-dark text-white text-sm font-semibold py-2.5 px-6 rounded-lg transition-all shadow-lg hover:shadow-primary/30 transform hover:-translate-y-0.5 hover:shadow-xl active:scale-95"
                        >
                            Get Started
                        </button>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
