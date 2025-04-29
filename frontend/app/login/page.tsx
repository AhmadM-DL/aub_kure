"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Header from "../ui/Header";
import Footer from "../ui/Footer";
import { unstable_noStore as noStore } from 'next/cache';

const LoginPage = () => {
  const router = useRouter();

  const [form, setForm] = useState({
    phone_number: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (!form.phone_number || !form.password) {
      setError("Phone number and password are required.");
      setLoading(false);
      return;
    }

    noStore();
    const host = process.env.NEXT_PUBLIC_ORCHESTRATOR_HOST;
    const port = process.env.NEXT_PUBLIC_ORCHESTRATOR_PORT;
    const orchestratorUrl = `http://${host}:${port}/login`;

    try {
      const response = await fetch(orchestratorUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          phone_number: form.phone_number,
          password: form.password,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.message || "Login failed.");
        setLoading(false);
        return;
      }

      router.push("/home");
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message || "Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header headerState='empty' />

      <main className="flex items-center justify-center pt-24 px-4">
        <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
          <h2 className="text-2xl font-bold text-black mb-6 text-center">Login</h2>

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
              <input
                type="tel"
                name="phone_number"
                value={form.phone_number}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            {error && <p className="text-red-500 text-sm">{error}</p>}

            <button
              type="submit"
              className="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800 transition cursor-pointer"
              disabled={loading}
            >
              {loading ? 'Logging In...' : 'Login'}
            </button>
          </form>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default LoginPage;
