import React, { useState, useEffect } from "react";

// Types for our data structures
interface Question {
  uid: string;
  domain: string;
  question: string;
  options: string[];
}

interface AssessmentResult {
  overall_score: number;
  confidence_score: number;
  domain_accuracy: Record<string, number>;
  weak_areas: string[];
  strong_areas: string[];
  tag_accuracy: Record<string, number>;
}

interface VideoResource {
  title: string;
  url: string;
}

interface Certification {
  title: string;
  provider: string;
  url: string;
}

const CareerReadinessApp: React.FC = () => {
  const [domains, setDomains] = useState<string[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [results, setResults] = useState<AssessmentResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Available domains
  const availableDomains = ["Python", "DSA", "SQL", "Communication"];

  // Handle domain selection
  const handleDomainChange = (domain: string) => {
    if (domains.includes(domain)) {
      setDomains(domains.filter((d) => d !== domain));
    } else {
      setDomains([...domains, domain]);
    }
  };

  // Start assessment
  const startAssessment = async () => {
    if (domains.length === 0) return;

    setIsLoading(true);
    // In a real app, this would call the backend API
    // For now, we'll simulate loading questions
    setTimeout(() => {
      // Mock questions data
      const mockQuestions: Question[] = domains.flatMap((domain) =>
        Array.from({ length: 3 }, (_, i) => ({
          uid: `${domain.toLowerCase()}-${i}`,
          domain,
          question: `Sample ${domain} question ${i + 1}?`,
          options: [
            `Option A for ${domain} question ${i + 1}`,
            `Option B for ${domain} question ${i + 1}`,
            `Option C for ${domain} question ${i + 1}`,
            `Option D for ${domain} question ${i + 1}`,
          ],
        }))
      );

      setQuestions(mockQuestions);
      setAnswers({});
      setSubmitted(false);
      setResults(null);
      setIsLoading(false);
    }, 1000);
  };

  // Handle answer selection
  const handleAnswerChange = (questionUid: string, answer: string) => {
    setAnswers({
      ...answers,
      [questionUid]: answer,
    });
  };

  // Submit assessment
  const submitAssessment = () => {
    setIsLoading(true);
    // In a real app, this would send answers to backend and receive results
    // For now, we'll simulate results
    setTimeout(() => {
      const mockResults: AssessmentResult = {
        overall_score: Math.floor(Math.random() * 40) + 60, // Random 60-100
        confidence_score: Math.floor(Math.random() * 30) + 70, // Random 70-100
        domain_accuracy: {
          Python: Math.floor(Math.random() * 40) + 60,
          DSA: Math.floor(Math.random() * 40) + 60,
          SQL: Math.floor(Math.random() * 40) + 60,
          Communication: Math.floor(Math.random() * 40) + 60,
        },
        weak_areas: [
          "Time Management",
          "Advanced Algorithms",
          "Database Design",
        ],
        strong_areas: ["Basic Syntax", "Communication Skills"],
        tag_accuracy: {
          "basic-concepts": Math.floor(Math.random() * 30) + 70,
          "intermediate-topics": Math.floor(Math.random() * 30) + 50,
          "advanced-topics": Math.floor(Math.random() * 40) + 30,
        },
      };

      setResults(mockResults);
      setSubmitted(true);
      setIsLoading(false);
    }, 1500);
  };

  // Reset assessment
  const resetAssessment = () => {
    setDomains([]);
    setQuestions([]);
    setAnswers({});
    setSubmitted(false);
    setResults(null);
  };

  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark text-gray-900 dark:text-gray-100 transition-colors duration-500">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-primary to-primary-dark bg-clip-text text-transparent">
            Career Readiness Diagnostic Platform
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            ML-powered assessment with learning & certification guidance
          </p>
        </header>

        {/* Loading indicator */}
        {isLoading && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-card-dark p-8 rounded-xl shadow-2xl">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-center">Processing...</p>
            </div>
          </div>
        )}

        {/* Domain Selection Section */}
        {!submitted && questions.length === 0 && (
          <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 mb-8 border border-gray-200 dark:border-border-dark transition-all hover:shadow-2xl">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
              Select Assessment Domains
            </h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              {availableDomains.map((domain) => (
                <div
                  key={domain}
                  className={`p-4 rounded-lg cursor-pointer transition-all border-2 ${
                    domains.includes(domain)
                      ? "border-primary bg-primary/10 text-primary"
                      : "border-gray-200 dark:border-border-dark hover:border-primary/50"
                  }`}
                  onClick={() => handleDomainChange(domain)}
                >
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      checked={domains.includes(domain)}
                      onChange={() => {}}
                      className="mr-3 h-5 w-5 rounded border-gray-300 text-primary focus:ring-primary"
                    />
                    <span className="font-medium">{domain}</span>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={startAssessment}
              disabled={domains.length === 0}
              className={`px-8 py-3 rounded-lg font-semibold text-white shadow-lg transition-all ${
                domains.length === 0
                  ? "bg-gray-400 cursor-not-allowed"
                  : "bg-primary hover:bg-primary-dark hover:shadow-primary/30 transform hover:-translate-y-0.5 active:scale-95"
              }`}
            >
              <span className="flex items-center">
                <span className="mr-2">🚀</span> Start Assessment
              </span>
            </button>
          </div>
        )}

        {/* Assessment Questions Section */}
        {!submitted && questions.length > 0 && (
          <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 mb-8 border border-gray-200 dark:border-border-dark">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
              Assessment
            </h2>

            <div className="mb-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <p className="text-lg font-medium text-blue-800 dark:text-blue-200">
                Total Questions: {questions.length}
              </p>
            </div>

            <div className="space-y-8">
              {questions.map((question) => (
                <div
                  key={question.uid}
                  className="p-5 bg-gray-50 dark:bg-surface-dark rounded-xl border border-gray-200 dark:border-border-dark"
                >
                  <div className="mb-4">
                    <span className="inline-block px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium">
                      [{question.domain}]
                    </span>
                    <h3 className="text-lg font-medium mt-2 text-gray-800 dark:text-gray-200">
                      {question.question}
                    </h3>
                  </div>

                  <div className="space-y-3">
                    {question.options.map((option, idx) => (
                      <div
                        key={idx}
                        className={`p-3 rounded-lg cursor-pointer transition-all ${
                          answers[question.uid] === option
                            ? "bg-primary/10 border-l-4 border-primary"
                            : "hover:bg-gray-100 dark:hover:bg-gray-800/50"
                        }`}
                        onClick={() => handleAnswerChange(question.uid, option)}
                      >
                        <div className="flex items-center">
                          <input
                            type="radio"
                            name={question.uid}
                            checked={answers[question.uid] === option}
                            onChange={() => {}}
                            className="mr-3 h-4 w-4 text-primary focus:ring-primary"
                          />
                          <span>{option}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 flex justify-end">
              <button
                onClick={submitAssessment}
                disabled={Object.keys(answers).length === 0}
                className={`px-8 py-3 rounded-lg font-semibold text-white shadow-lg transition-all ${
                  Object.keys(answers).length === 0
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-primary hover:bg-primary-dark hover:shadow-primary/30 transform hover:-translate-y-0.5 active:scale-95"
                }`}
              >
                Submit Assessment
              </button>
            </div>
          </div>
        )}

        {/* Results Section */}
        {submitted && results && (
          <div className="space-y-8">
            {/* Overall Performance Metrics */}
            <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-border-dark">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white flex items-center">
                <span className="mr-3">📊</span> Overall Performance
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gradient-to-br from-primary/10 to-primary/5 dark:from-primary/10 dark:to-primary/5 p-6 rounded-xl border border-primary/20">
                  <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Overall Readiness
                  </h3>
                  <p className="text-4xl font-bold text-primary">
                    {results.overall_score}%
                  </p>
                </div>

                <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900/20 dark:to-emerald-800/20 p-6 rounded-xl border border-emerald-200 dark:border-emerald-800">
                  <h3 className="text-lg font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Confidence Score
                  </h3>
                  <p className="text-4xl font-bold text-emerald-600 dark:text-emerald-400">
                    {results.confidence_score}%
                  </p>
                </div>
              </div>
            </div>

            {/* Domain-wise Performance */}
            <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-border-dark">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
                Domain-wise Performance
              </h2>

              <div className="space-y-4">
                {Object.entries(results.domain_accuracy).map(
                  ([domain, score]) => (
                    <div key={domain}>
                      <div className="flex justify-between mb-1">
                        <span className="font-medium text-gray-700 dark:text-gray-300">
                          {domain}
                        </span>
                        <span className="text-gray-600 dark:text-gray-400">
                          {score}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4">
                        <div
                          className="bg-primary h-4 rounded-full transition-all duration-1000 ease-out"
                          style={{ width: `${score}%` }}
                        ></div>
                      </div>
                    </div>
                  )
                )}
              </div>
            </div>

            {/* Diagnostic Insights */}
            <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-border-dark">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
                Diagnostic Insights
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                    <span className="mr-2">⚠️</span> Weak Areas
                  </h3>
                  <ul className="space-y-2">
                    {results.weak_areas.length > 0 ? (
                      results.weak_areas.map((area, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="text-red-500 mr-2">•</span>
                          <span className="text-gray-700 dark:text-gray-300">
                            {area}
                          </span>
                        </li>
                      ))
                    ) : (
                      <li className="text-gray-500 italic">
                        No weak areas identified
                      </li>
                    )}
                  </ul>
                </div>

                <div>
                  <h3 className="text-xl font-semibold mb-4 text-green-600 dark:text-green-400 flex items-center">
                    <span className="mr-2">✅</span> Strong Areas
                  </h3>
                  <ul className="space-y-2">
                    {results.strong_areas.length > 0 ? (
                      results.strong_areas.map((area, idx) => (
                        <li key={idx} className="flex items-start">
                          <span className="text-green-500 mr-2">•</span>
                          <span className="text-gray-700 dark:text-gray-300">
                            {area}
                          </span>
                        </li>
                      ))
                    ) : (
                      <li className="text-gray-500 italic">
                        No strong areas identified
                      </li>
                    )}
                  </ul>
                </div>
              </div>
            </div>

            {/* Learning Resources */}
            <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-border-dark">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white flex items-center">
                <span className="mr-3">🎥</span> Learning Resources
              </h2>

              <div className="space-y-4">
                {Array.from({ length: 3 }, (_, idx) => (
                  <div
                    key={idx}
                    className="p-4 bg-gray-50 dark:bg-surface-dark rounded-lg border border-gray-200 dark:border-border-dark"
                  >
                    <h3 className="font-medium text-gray-800 dark:text-gray-200">
                      Sample Resource Title {idx + 1}
                    </h3>
                    <a
                      href="#"
                      className="text-primary hover:underline mt-1 inline-block"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Watch Resource
                    </a>
                  </div>
                ))}
              </div>
            </div>

            {/* Certification Roadmap */}
            <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-border-dark">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white flex items-center">
                <span className="mr-3">🎓</span> Certification Roadmap
              </h2>

              <div className="mb-8">
                <h3 className="text-xl font-semibold mb-4 text-blue-600 dark:text-blue-400">
                  Compulsory Certifications (Mandatory Baseline)
                </h3>

                <div className="space-y-4">
                  {Array.from({ length: 2 }, (_, idx) => (
                    <div
                      key={idx}
                      className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800"
                    >
                      <h4 className="font-medium text-gray-800 dark:text-gray-200">
                        Sample Compulsory Certification {idx + 1}
                      </h4>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        Provider: Sample Provider
                      </p>
                      <a
                        href="#"
                        className="text-primary hover:underline mt-2 inline-block"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        View Certification
                      </a>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-4 text-purple-600 dark:text-purple-400">
                  Personalized Certifications (ML-powered)
                </h3>

                <div className="space-y-4">
                  {Array.from({ length: 3 }, (_, idx) => (
                    <div
                      key={idx}
                      className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800"
                    >
                      <h4 className="font-medium text-gray-800 dark:text-gray-200">
                        Sample Personalized Certification {idx + 1}
                      </h4>
                      <p className="text-gray-600 dark:text-gray-400 text-sm">
                        Provider: Sample Provider
                      </p>
                      <a
                        href="#"
                        className="text-primary hover:underline mt-2 inline-block"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        View Certification
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Study Plan */}
            <div className="bg-white dark:bg-card-dark rounded-2xl shadow-xl p-6 border border-gray-200 dark:border-border-dark">
              <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white">
                7-Day Study Plan
              </h2>

              <div className="space-y-4">
                {Array.from({ length: 7 }, (_, idx) => (
                  <div
                    key={idx}
                    className="p-4 bg-gray-50 dark:bg-surface-dark rounded-lg border border-gray-200 dark:border-border-dark"
                  >
                    <h3 className="font-medium text-gray-800 dark:text-gray-200">
                      Day {idx + 1}: Focus on{" "}
                      <span className="text-primary">
                        Sample Topic {idx + 1}
                      </span>
                    </h3>
                  </div>
                ))}
              </div>
            </div>

            {/* Reset Button */}
            <div className="text-center mt-8">
              <button
                onClick={resetAssessment}
                className="px-6 py-3 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg font-medium transition-colors"
              >
                Take Another Assessment
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CareerReadinessApp;
