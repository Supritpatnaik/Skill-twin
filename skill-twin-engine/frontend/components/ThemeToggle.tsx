
import React from 'react';

interface ThemeToggleProps {
  isDarkMode: boolean;
  toggleTheme: () => void;
}

const ThemeToggle: React.FC<ThemeToggleProps> = ({ isDarkMode, toggleTheme }) => {
  return (
    <button
      onClick={toggleTheme}
      aria-label="Toggle Dark Mode"
      className={`relative inline-flex items-center h-8 w-14 rounded-full transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary ${isDarkMode ? 'bg-primary' : 'bg-gray-300 dark:bg-gray-700'}`}
    >
      <span className="sr-only">Toggle theme</span>
      <span
        className={`inline-flex items-center justify-center h-6 w-6 transform bg-white dark:bg-gray-900 rounded-full transition-transform duration-300 ease-in-out shadow-md ${
          isDarkMode ? 'translate-x-7' : 'translate-x-1'
        }`}
      >
        <span className={`material-icons text-sm transition-opacity duration-200 ${isDarkMode ? 'opacity-100 text-yellow-400' : 'opacity-0'}`}>light_mode</span>
        <span className={`material-icons text-sm absolute transition-opacity duration-200 ${!isDarkMode ? 'opacity-100 text-gray-500' : 'opacity-0'}`}>dark_mode</span>
      </span>
    </button>
  );
};

export default ThemeToggle;
