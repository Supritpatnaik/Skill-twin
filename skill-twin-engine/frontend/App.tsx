
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import FeaturesSection from './components/FeaturesSection';
import HowItWorksSection from './components/HowItWorksSection';
import ProblemSolutionSection from './components/ProblemSolutionSection';
import ImpactSection from './components/ImpactSection';
import Footer from './components/Footer';
import DashboardPage from './components/DashboardPage';

const App: React.FC = () => {
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [page, setPage] = useState('landing'); // 'landing' or 'dashboard'

    useEffect(() => {
        const savedTheme = localStorage.getItem('theme');
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (savedTheme === 'dark' || (!savedTheme && systemDark)) {
            document.documentElement.classList.add('dark');
            setIsDarkMode(true);
        } else {
            document.documentElement.classList.remove('dark');
            setIsDarkMode(false);
        }
    }, []);

    const toggleTheme = () => {
        setIsDarkMode(prevMode => {
            const newMode = !prevMode;
            if (newMode) {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            }
            return newMode;
        });
    };

    const navigateToDashboard = () => {
        setPage('dashboard');
    };

    const navigateToLanding = () => {
        setPage('landing');
    }

    if (page === 'dashboard') {
        return <DashboardPage isDarkMode={isDarkMode} toggleTheme={toggleTheme} onLogoClick={navigateToLanding} />;
    }

    // App.tsx - Line 57
return (
    <>
        <Header isDarkMode={isDarkMode} toggleTheme={toggleTheme} onGetStartedClick={navigateToDashboard} />
        {/* ADD: relative z-10 and ensure solid bg classes */}
        <main className="relative z-10 pt-24 bg-background-light dark:bg-background-dark shadow-2xl pb-20 mb-[100vh]">
            {/* Background Blobs */}
            <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
                {/* ... existing blob code */}
            </div>
            
            <HeroSection onCheckReadinessClick={navigateToDashboard} />
            <FeaturesSection />
            <HowItWorksSection />
            <ProblemSolutionSection />
            <ImpactSection />
        </main>
        <Footer />
    </>
);
};

export default App;
