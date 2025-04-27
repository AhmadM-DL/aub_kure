const Features = () => {
    return (
      <section id="features" className="w-full bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-black mb-8 text-center">
            What Makes Kure Unique?
          </h2>
  
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            {/* Feature 1 */}
            <div className="bg-white shadow-sm p-6 rounded-md hover:shadow-md transition">
              <h3 className="text-xl font-semibold text-black mb-2">Send Voice Notes via WhatsApp</h3>
              <p className="text-gray-700">
                Use WhatsApp to send your thoughts as voice notes — no need to download a new app or change your habits.
              </p>
            </div>
  
            {/* Feature 2 */}
            <div className="bg-white shadow-sm p-6 rounded-md hover:shadow-md transition">
              <h3 className="text-xl font-semibold text-black mb-2">AI-Powered Transcription</h3>
              <p className="text-gray-700">
                Your voice notes are automatically transcribed using advanced AI, making your ideas easy to read and revisit.
              </p>
            </div>
  
            {/* Feature 3 */}
            <div className="bg-white shadow-sm p-6 rounded-md hover:shadow-md transition">
              <h3 className="text-xl font-semibold text-black mb-2">Track Mood & Suicidal Thoughts</h3>
              <p className="text-gray-700">
                Kure detects emotional patterns and signs of distress, offering a dashboard to help you understand your mental health over time.
              </p>
            </div>
          </div>
        </div>
      </section>
    );
  };
  
  export default Features;
  