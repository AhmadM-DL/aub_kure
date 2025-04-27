"use client";
import { useState } from "react";
import Header from "../ui/Header";
import Footer from "../ui/Footer";
import { unstable_noStore as noStore } from 'next/cache';

const SignUpPage = () => {
  const [form, setForm] = useState({
    email: "",
    phone_number: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const isEmailValid = (email: string) => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);

  const isPasswordValid = (password: string) => {
    const regex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d@$!%*?&]{8,}$/;
    return regex.test(password);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);

    if (!isEmailValid(form.email)) {
      setError("Please enter a valid email address.");
      setLoading(false);
      return;
    }

    if (!isPasswordValid(form.password)) {
      setError("Password must be at least 8 characters long, contain an uppercase letter, a number, and a special character.");
      setLoading(false);
      return;
    }

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }

    noStore();
    const host = process.env.NEXT_PUBLIC_ORCHESTRATOR_HOST;
    const port = process.env.NEXT_PUBLIC_ORCHESTRATOR_PORT;
    const orchestratorUrl = `http://${host}:${port}/register`;

    try {
      const response = await fetch(orchestratorUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: form.email,
          phone_number: form.phone_number,
          password: form.password,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.message || "Signup failed.");
        setLoading(false);
        return;
      }

      setSuccess(true);
      setForm({ email: "", phone_number: "", password: "", confirmPassword: "" });
    } catch (err: unknown) {
    if (err instanceof Error) {
      setError(err.message || "Something went wrong. Please try again.");
    }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="flex items-center justify-center pt-24 px-4">
        <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md sm:max-w-lg md:max-w-xl lg:max-w-[35%]">
          <h2 className="text-2xl font-bold text-black mb-6 text-center">Create an Account</h2>

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

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

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                value={form.confirmPassword}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-black"
              />
            </div>

            {error && <p className="text-red-500 text-sm">{error}</p>}
            {success && <p className="text-green-600 text-sm">Signup successful!</p>}

            <button
              type="submit"
              className="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800 transition"
              disabled={loading}
            >
              {loading ? 'Signing Up...' : 'Sign Up'}
            </button>
          </form>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default SignUpPage;
