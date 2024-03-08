"use client";

import Image from "next/image";
import React from "react";
import { BackgroundBeams } from "@/components/ui/background-beams";
import { CardStack, Card } from "@/components/ui/card-stack";
import { cn } from "@/lib/utils/cn";

export const Highlight = ({
	children,
	className,
}: {
	children: React.ReactNode;
	className?: string;
}) => {
	return (
		<span
			className={cn(
				"font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-700/[0.2] dark:text-emerald-500 px-1 py-0.5",
				className
			)}
		>
			{children}
		</span>
	);
};

const CARDS:Card[] = [
    {
        id: 1,
        question: "Gender",
        inputType: "radio",
        feature_name: "gender",
        options: [{label: "Male", value: "Male"}, {label: "Female", value: "Female"}]
    },
    {
        id: 2,
        question: "Age",
        inputType: "number",
        feature_name: "age"
    },
    {
        id: 3,
        question: "School Year",
        inputType: "radio",
        feature_name: "school_year",
        options: [
            {label: "1", value: "1"}, 
            {label: "2", value: "2"}, 
            {label: "3", value: "3"}, 
            {label: "4", value: "4"}
        ]
    },
];

/*
<input
	type="radio" >
	id="anxietySeverityMild" >
	name="anxiety_severity" >
	value="Mild"
/>
<label for="anxietySeverityMild">Mild</label><br />
*/

const onCardSubmit = (formData: any) => {
	console.log("Form Data: ", formData);
	// Post formData to an API endpoint
	fetch("/your-api-endpoint", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(formData),
	})
		.then((response) => response.json())
		.then((data) => console.log(data))
		.catch((error) => console.error("Error:", error));
};

export default function Home() {
	return (
		<div className="">
			<form className="h-[40rem] flex items-center justify-center w-full">
				<CardStack items={CARDS} onCardSubmit={onCardSubmit} />
			</form>
			<BackgroundBeams />
		</div>
	);
}
