"use client";

import Image from "next/image";
import React, { useState } from "react";
import { cn } from "@/lib/utils/cn";
import { motion } from "framer-motion";

import { BackgroundBeams } from "@/components/ui/background-beams";
import { CardStack, Card } from "@/components/ui/card-stack";
import { BentoGrid, BentoGridItem } from "@/components/ui/bento-grid";
import * as Tabler from "@tabler/icons-react";

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

const CARDS: Card[] = [
	{
		id: 1,
		question: "What is your gender?",
		inputType: "radio",
		feature_name: "gender",
		options: [
			{ label: "Male", value: "Male" },
			{ label: "Female", value: "Female" },
		],
		done: false,
	},
	{
		id: 2,
		question: "How old are you?",
		inputType: "number",
		feature_name: "age",
		done: false,
	},
	{
		id: 3,
		question: "What school year are you in?",
		inputType: "radio",
		feature_name: "school_year",
		options: [
			{ label: "1", value: "1" },
			{ label: "2", value: "2" },
			{ label: "3", value: "3" },
			{ label: "4 or N/A", value: "4" },
		],
		done: false,
	},
	{
		id: 4,
		question: "How many hours do you sleep?",
		inputType: "number",
		feature_name: "sleep_hours",
		done: false,
	},
	{
		id: 5,
		question: "How many friends do you have?",
		inputType: "number",
		feature_name: "number_of_friends",
		done: false,
	},
	{
		id: 6,
		question: "What is your PHQ Score? (0 if you don't know)",
		inputType: "number",
		feature_name: "phq_score",
		done: false,
	},
	{
		id: 7,
		question: "What is your GAD Score? (0 if you don't know)",
		inputType: "number",
		feature_name: "gad_score",
		done: false,
	},
	{
		id: 8,
		question: "What is your Epworth Score? (0 if you don't know)",
		inputType: "number",
		feature_name: "epworth_score",
		done: false,
	},
	{
		id: 9,
		question: "What is your BMI (0 if not applicable)",
		inputType: "number",
		feature_name: "bmi",
		done: false,
	},
	{
		id: 10,
		question: "Do you feel depressed?",
		inputType: "radio",
		feature_name: "depressiveness",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 11,
		question: "Do you feel suicidal?",
		inputType: "radio",
		feature_name: "suicidal",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 12,
		question: "Do you have treatment for depression?",
		inputType: "radio",
		feature_name: "depression_treatment",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 13,
		question: "Do you often feel anxious?",
		inputType: "radio",
		feature_name: "anxiousness",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 14,
		question: "Are you diagnosed with anxiety?",
		inputType: "radio",
		feature_name: "anxiety_diagnosis",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 15,
		question: "Are you prescribed anxiety treatments?",
		inputType: "radio",
		feature_name: "anxiety_treatment",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 16,
		question: "Are you often sleepy?",
		inputType: "radio",
		feature_name: "sleepiness",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 17,
		question: "Do you like presentations?",
		inputType: "radio",
		feature_name: "likes_presentations",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 18,
		question: "Do you like new things?",
		inputType: "radio",
		feature_name: "likes_new_things",
		options: [
			{ label: "Yes", value: "Yes" },
			{ label: "No", value: "No" },
		],
		done: false,
	},
	{
		id: 19,
		question: "Do you feel anxious?",
		inputType: "radio",
		feature_name: "feeling_anxious",
		options: [
			{ label: "Often/Always", value: "1" },
			{ label: "Rarely/Sometimes", value: "0" },
		],
		done: false,
	},
	{
		id: 20,
		question: "Rate your depression severity",
		inputType: "radio",
		feature_name: "depression_severity",
		options: [
			{ label: "None/Minimal", value: "None-minimal" },
			{ label: "Moderate", value: "Moderate" },
			{ label: "Moderately severe", value: "Moderately severe" },
			{ label: "Severe", value: "Severe" },
		],
		done: false,
	},
	{
		id: 21,
		question: "Rate your anxiety severity",
		inputType: "radio",
		feature_name: "anxiety_severity",
		options: [
			{ label: "Mild", value: "Mild" },
			{ label: "Moderate", value: "Moderate" },
			{ label: "None-minimal", value: "None-minimal" },
			{ label: "Severe", value: "Severe" },
		],
		done: false,
	},
	{
		id: 22,
		question: "Do you take notes?",
		inputType: "radio",
		feature_name: "note_taking",
		options: [
			{ label: "Rarely/Sometimes", value: "Sometimes" },
			{ label: "Often/Always", value: "Always" },
		],
		done: false,
	},
	{
		id: 23,
		question: "Do you face academic challenges?",
		inputType: "radio",
		feature_name: "academic_challenges",
		options: [
			{ label: "Rarely/Sometimes", value: "No" },
			{ label: "Often/Always", value: "Yes" },
		],
		done: false,
	},
	{
		id: 24,
		question: "Do you feel sad?",
		inputType: "radio",
		feature_name: "feeling_sad",
		options: [
			{ label: "Rarely/Sometimes", value: "0" },
			{ label: "Often", value: "1" },
			{ label: "Always", value: "2" },
		],
		done: false,
	},
	{
		id: 25,
		question: "Do you have trouble sleeping?",
		inputType: "radio",
		feature_name: "trouble_sleeping",
		options: [
			{ label: "Rarely", value: "0" },
			{ label: "Sometimes", value: "1" },
			{ label: "Often", value: "2" },
		],
		done: false,
	},
	{
		id: 26,
		question: "Do you feel you overeat?",
		inputType: "radio",
		feature_name: "overeating",
		options: [
			{ label: "Rarely", value: "0" },
			{ label: "Sometimes", value: "1" },
			{ label: "Often", value: "2" },
		],
		done: false,
	},
	{
		id: 27,
		question: "Do you feel guilty?",
		inputType: "radio",
		feature_name: "feeling_guilt",
		options: [
			{ label: "Rarely", value: "0" },
			{ label: "Sometimes", value: "1" },
			{ label: "Often", value: "2" },
			{ label: "Always", value: "3" },
		],
		done: false,
	},
	{
		id: 28,
		question: "Do you have trouble concentrating?",
		inputType: "radio",
		feature_name: "problems_concentrating",
		options: [
			{ label: "Rarely", value: "0" },
			{ label: "Sometimes", value: "1" },
			{ label: "Often", value: "2" },
			{ label: "Always", value: "3" },
		],
		done: false,
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

type Recommendation = {
	id: string; // dont mind this
	title: string; // title of the recommendation
	description: string; // full description of the recommendation
	icon: string; // choose from https://tabler-icons-react.vercel.app/
	url: string; // url to the webpage source of this recommendation
	trigger: { label: string; value: string }[]; // array of all questions that trigger to recommend this
};

type Results = {
	is_depressed: string;
	recommendations: Recommendation[];
};

const IconMapping: { [key: string]: JSX.Element } = {
	IconStretching: (
		<Tabler.IconStretching className="h-4 w-4 text-neutral-500" />
	),
	IconActivityHeartbeat: (
		<Tabler.IconActivityHeartbeat className="h-4 w-4 text-neutral-500" />
	),
	IconUserSearch: (
		<Tabler.IconUserSearch className="h-4 w-4 text-neutral-500" />
	),
	IconMoonStars: <Tabler.IconMoonStars className="h-4 w-4 text-neutral-500" />,
	IconCarrot: <Tabler.IconCarrot className="h-4 w-4 text-neutral-500" />,
	IconUsers: <Tabler.IconUsers className="h-4 w-4 text-neutral-500" />,
	IconLeaf: <Tabler.IconLeaf className="h-4 w-4 text-neutral-500" />,
	IconBrain: <Tabler.IconBrain className="h-4 w-4 text-neutral-500" />,
	IconTarget: <Tabler.IconTarget className="h-4 w-4 text-neutral-500" />,
	IconCalendar: <Tabler.IconCalendar className="h-4 w-4 text-neutral-500" />,
	IconRun: <Tabler.IconRun className="h-4 w-4 text-neutral-500" />,
	IconMessageCircle: (
		<Tabler.IconMessageCircle className="h-4 w-4 text-neutral-500" />
	),
	IconDeviceFloppy: (
		<Tabler.IconDeviceFloppy className="h-4 w-4 text-neutral-500" />
	),
	IconPalette: <Tabler.IconPalette className="h-4 w-4 text-neutral-500" />,
	IconGrillFork: <Tabler.IconGrillFork className="h-4 w-4 text-neutral-500" />,
	IconNotebook: <Tabler.IconNotebook className="h-4 w-4 text-neutral-500" />,
	IconHandStop: <Tabler.IconHandStop className="h-4 w-4 text-neutral-500" />,
	IconBulb: <Tabler.IconBulb className="h-4 w-4 text-neutral-500" />,
	IconBedOff: <Tabler.IconBedOff className="h-4 w-4 text-neutral-500" />,
	IconSun: <Tabler.IconSun className="h-4 w-4 text-neutral-500" />,
	IconBook: <Tabler.IconBook className="h-4 w-4 text-neutral-500" />,
	IconSchool: <Tabler.IconSchool className="h-4 w-4 text-neutral-500" />,
	IconBallBasketball: <Tabler.IconBallBasketball className="h-4 w-4 text-neutral-500" />,
	IconLayout: <Tabler.IconLayout className="h-4 w-4 text-neutral-500" />,
	IconReportMedical: <Tabler.IconReportMedical className="h-4 w-4 text-neutral-500" />,
	IconWind: <Tabler.IconWind className="h-4 w-4 text-neutral-500" />,
	IconHomeHeart: <Tabler.IconHomeHeart className="h-4 w-4 text-neutral-500" />,
	IconHealthRecoginition: <Tabler.IconHealthRecognition className="h-4 w-4 text-neutral-500" />,
	IconBellSchool: <Tabler.IconBellSchool className="h-4 w-4 text-neutral-500" />,
	IconZoomQuestion: <Tabler.IconZoomQuestion className="h-4 w-4 text-neutral-500" />,
	IconPuzzle: <Tabler.IconPuzzle className="h-4 w-4 text-neutral-500" />,
	IconMicrophone: <Tabler.IconMicrophone className="h-4 w-4 text-neutral-500" />,
	IconShieldCheck: <Tabler.IconShieldCheck className="h-4 w-4 text-neutral-500" />,
	IconAccessible: <Tabler.IconAccessible className="h-4 w-4 text-neutral-500" />,
	IconGrowth: <Tabler.IconGrowth className="h-4 w-4 text-neutral-500" />,
	IconFish: <Tabler.IconFish className="h-4 w-4 text-neutral-500" />,
};

const ShowResults = ({
	verdict,
	items,
	selectedId,
	setSelectedId,
}: {
	verdict: string;
	items: Recommendation[];
	selectedId: string;
	setSelectedId: (id: string) => void;
}) => {
	return (
		<BentoGrid className="max-w-4xl mx-auto">
			{items.map((item) => (
				<motion.div
					key={item?.id}
					layoutId={item?.id}
					onClick={() => setSelectedId(item?.id)}
				>
					<BentoGridItem
						title={item.title}
						description={item.description}
						className={"border border-gray"}
						icon={IconMapping[item.icon]}
						url={item.url}
					/>
					{/* <motion.h5>
						{item?.subtitle}
					</motion.h5>
					<motion.h2>
						{item?.title}
					</motion.h2> */}
				</motion.div>
			))}
		</BentoGrid>
	);
};

export default function Home() {
	const [data, setData] = useState<Results>({
		is_depressed: "",
		recommendations: [],
	});
	const [selectedId, setSelectedId] = useState<string>("0");
	const [isSubmitted, setIsSubmitted] = useState(false);

	const onCardSubmit = (formData: any) => {
		console.log("Form Data: ", formData);
		// Post formData to an API endpoint
		fetch("http://127.0.0.1:8000/result/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(formData),
		})
			.then((response) => response.json())
			.then((data) => {
				console.log(data);
				setData(data);
				setIsSubmitted(true);
			})
			.catch((error) => console.error("Error:", error));
	};

	return (
		<>
			{!isSubmitted && (
				<>
					<motion.div
						initial={{ opacity: 0 }} // Add opacity: 0 to initial state
						animate={{ opacity: 1 }} // Add opacity: 1 to animate state
						transition={{ duration: 1 }} // Add delay: 0.5 to the transition object
						className=""
					>
						<div className="flex items-center justify-center w-full">
							<h1 className="text-3xl font-bold text-center mt-10">
								Welcome to the Mental Health Assessment Tool
							</h1>
						</div>
						<div>
							<h3 className="text-center mt-1">
								Tell us about yourself. Answer the all questions honestly.
							</h3>
						</div>
					</motion.div>
					<motion.div
						initial={{ opacity: 0 }} // Add opacity: 0 to initial state
						animate={{ opacity: 1 }} // Add opacity: 1 to animate state
						transition={{ duration: 2, delay: 1.5 }} // Add delay: 1 to the transition object
						className=""
					>
						<form className="mt-20 flex items-center justify-center w-full">
							<CardStack items={CARDS} onCardSubmit={onCardSubmit} />
						</form>
					</motion.div>
				</>
			)}
			{isSubmitted && data && (
				<>
					<motion.div
						initial={{ opacity: 0 }} // Add opacity: 0 to initial state
						animate={{ opacity: 1 }} // Add opacity: 1 to animate state
						transition={{ duration: 1 }} // Add delay: 0.5 to the transition object
						className=""
					>
						<div className="flex items-center justify-center w-full">
							<h1 className="text-3xl font-bold text-center mt-10">
								{(() => {
									let message;

									switch (data.is_depressed) {
										case "0":
											message = "You are doing well!";
											break;
										case "1":
											message = "You are doing well!";
											break;
										case "2":
											message = "You are not doing so well...";
											break;
										case "3":
											message = "You are not doing so well...";
											break;
										default:
											message = "You are doing well!";
											break;
									}
									return message;
								})()}
							</h1>
						</div>
						<div>
							<h3 className="text-center mt-1">
								Consider these tips to help you with your mental health
							</h3>
						</div>
					</motion.div>
					<motion.div
						initial={{ opacity: 0 }} // Add opacity: 0 to initial state
						animate={{ opacity: 1 }} // Add opacity: 1 to animate state
						transition={{ duration: 2, delay: 1.5 }} // Add delay: 1 to the transition object
						className=""
					>
						<div className="mt-10 w-full">
							<ShowResults
								verdict={data.is_depressed}
								items={data.recommendations}
								selectedId={selectedId}
								setSelectedId={setSelectedId}
							/>
						</div>
					</motion.div>
					<div className="mt-32 w-full"/>
				</>
			)}
			{<BackgroundBeams />}
		</>
	);
}
