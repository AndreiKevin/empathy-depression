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
        options: [{label: "Male", value: "Male"}, {label: "Female", value: "Female"}],
		done: false
    },
    {
        id: 2,
        question: "Age",
        inputType: "number",
        feature_name: "age",
		done: false
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
        ],
		done: false
    },
    {
        id: 4,
        question: "Sleep Hours",
        inputType: "number",
        feature_name: "sleep_hours",
		done: false
    },
    {
        id: 5,
        question: "Number of Friends",
        inputType: "number",
        feature_name: "number_of_friends",
		done: false
    },
    {
        id: 6,
        question: "PHQ Score",
        inputType: "number",
        feature_name: "phq_score",
		done: false
    },
    {
        id: 7,
        question: "GAD Score",
        inputType: "number",
        feature_name: "gad_score",
		done: false
    },
    {
        id: 8,
        question: "Epworth Score",
        inputType: "number",
        feature_name: "epworth_score",
		done: false
    },
    {
        id: 9,
        question: "BMI",
        inputType: "number",
        feature_name: "bmi",
		done: false
    },
    {
        id: 10,
        question: "Depressiveness",
        inputType: "radio",
        feature_name: "depressiveness",
        options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
    },
    {
        id: 11,
        question: "Suicidal",
        inputType: "radio",
        feature_name: "suicidal",
        options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
    },
    {
        id: 12,
        question: "Depression Treatment",
        inputType: "radio",
        feature_name: "depression_treatment",
        options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
    },
	{
		id: 13,
		question: "Anxiousness",
		inputType: "radio",
		feature_name: "anxiousness",
		options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
	},
	{
		id: 14,
		question: "Anxiety Diagnosis",
		inputType: "radio",
		feature_name: "anxiety_diagnosis",
		options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
	},
	{
		id: 15,
		question: "Anxiety Treatment",
		inputType: "radio",
		feature_name: "anxiety_treatment",
		options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
	},
	{
		id: 16,
		question: "Sleepiness",
		inputType: "radio",
		feature_name: "sleepiness",
		options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
	},
	{
		id: 17,
		question: "Likes Presentations",
		inputType: "radio",
		feature_name: "likes_presentations",
		options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
	},
	{
		id: 18,
		question: "Likes New Things",
		inputType: "radio",
		feature_name: "likes_new_things",
		options: [{label: "Yes", value: "Yes"}, {label: "No", value: "No"}],
		done: false
	},
	{
		id: 19,
		question: "Feeling Anxious",
		inputType: "radio",
		feature_name: "feeling_anxious",
		options: [
			{label: "Often/Always", value: "1"}, 
			{label: "Rarely/Sometimes", value: "0"}
		],
		done: false
	},
	{
		id: 20,
		question: "Depression Severity",
		inputType: "radio",
		feature_name: "depression_severity",
		options: [
			{label: "None/Minimal", value: "None-minimal"}, 
			{label: "Moderate", value: "Moderate"}, 
			{label: "Moderately severe", value: "Moderately severe"}, 
			{label: "Severe", value: "Severe"}
		],
		done: false
	},
	{
		id: 21,
		question: "Anxiety Severity",
		inputType: "radio",
		feature_name: "anxiety_severity",
		options: [
			{label: "Mild", value: "Mild"}, 
			{label: "Moderate", value: "Moderate"}, 
			{label: "None-minimal", value: "None-minimal"}, 
			{label: "Severe", value: "Severe"}
		],
		done: false
	},
	{
		id: 22,
		question: "Note Taking",
		inputType: "radio",
		feature_name: "note_taking",
		options: [
			{label: "Rarely/Sometimes", value: "Sometimes"}, 
			{label: "Often/Always", value: "Always"}
		],
		done: false
	},
	{
		id: 23,
		question: "Academic Challenges",
		inputType: "radio",
		feature_name: "academic_challenges",
		options: [
			{label: "Rarely/Sometimes", value: "No"}, 
			{label: "Often/Always", value: "Yes"}
		],
		done: false
	},
	{
		id: 24,
		question: "Feeling Sad",
		inputType: "radio",
		feature_name: "feeling_sad",
		options: [
			{label: "Rarely/Sometimes", value: "0"}, 
			{label: "Often", value: "1"}, 
			{label: "Always", value: "2"}
		],
		done: false
	},
	{
		id: 25,
		question: "Trouble Sleeping",
		inputType: "radio",
		feature_name: "trouble_sleeping",
		options: [
			{label: "Rarely", value: "0"}, 
			{label: "Sometimes", value: "1"}, 
			{label: "Often", value: "2"}
		],
		done: false
	},
	{
		id: 26,
		question: "Overeating",
		inputType: "radio",
		feature_name: "overeating",
		options: [
			{label: "Rarely", value: "0"}, 
			{label: "Sometimes", value: "1"}, 
			{label: "Often", value: "2"}
		],
		done: false
	},
	{
		id: 27,
		question: "Feeling Guilt",
		inputType: "radio",
		feature_name: "feeling_guilt",
		options: [
			{label: "Rarely", value: "0"}, 
			{label: "Sometimes", value: "1"}, 
			{label: "Often", value: "2"}, 
			{label: "Always", value: "3"}
		],
		done: false
	},
	{
		id: 28,
		question: "Problems Concentrating",
		inputType: "radio",
		feature_name: "problems_concentrating",
		options: [
			{label: "Rarely", value: "0"}, 
			{label: "Sometimes", value: "1"}, 
			{label: "Often", value: "2"}, 
			{label: "Always", value: "3"}
		],
		done: false
	}	
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
			{/*<BackgroundBeams />*/}
		</div>
	);
}
