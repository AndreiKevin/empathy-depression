"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

let interval: any;

export type Card = {
	id: number;
	question: string;
	inputType: string;
	feature_name: string; // name of the column in the machine learning model
	options?: {label:string, value:string}[]; // label--displayed to the user, value--sent to the server
};

export const CardStack = ({
	items,
	offset,
	scaleFactor,
	onCardSubmit,
}: {
	items: Card[];
	onCardSubmit: (formData: any) => void;
	offset?: number;
	scaleFactor?: number;
}) => {
	const CARD_OFFSET = offset || 10;
	const SCALE_FACTOR = scaleFactor || 0.06;
	const [cards, setCards] = useState<Card[]>(items);

	const [currentCardIndex, setCurrentCardIndex] = useState(0);
	const [formData, setFormData] = useState<Record<string, any>>({});

	const updateFormData = (key: string, value: any) => {
		setFormData({ ...formData, [key]: value });
	};

	const handleSubmit = (event: React.FormEvent) => {
		event.preventDefault();
		onCardSubmit?.(formData);
	};

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
		updateFormData(items[currentCardIndex].question, event.target.value);
	};

	const renderInputField = (card: Card) => {
		switch (card.inputType) {
			case "text":
				return (
					<Input
						type="text"
						value={formData[card.question] || ""}
						onChange={handleInputChange}
					/>
				);
			case "number":
				return (
					<Input
						className="remove-arrow"
						type="number"
						onChange={handleInputChange}
					/>
				);
			case "radio":
				return card.options?.map((option) => (
					<label className="mb-1" key={option.value}>
						<input
							type="radio"
							id={card.id.toString() + option.value}
							name={card.feature_name}
							value={option.value}
							onChange={handleInputChange}
						/> {option.label}
					</label>
				));				
			// Add more cases as needed for different input types
			default:
				return <input type="text" onChange={handleInputChange} />;
		}
	};

	const nextCardHandler = () => {
		if (currentCardIndex < items.length - 1) {
			startFlipping();
			setCurrentCardIndex(currentCardIndex + 1);
		} else {
			onCardSubmit(formData); 
		}
	};

	const startFlipping = () => {
		setCards((prevCards: Card[]) => {
			const newArray = [...prevCards]; // create a copy of the array
			newArray.unshift(newArray.pop()!); // move the last element to the front
			return newArray;
		});
	};

	return (
		<>
			<div className="relative h-60 w-60 md:h-60 md:w-96">
				{cards.map((card, index) => {
						return (
							<motion.div
								key={card.id}
								className="absolute dark:bg-black bg-white h-60 w-60 md:h-60 md:w-96 rounded-3xl p-4 shadow-xl border border-neutral-200 dark:border-white/[0.1]  shadow-black/[0.1] dark:shadow-white/[0.05] flex flex-col"
								style={{
									transformOrigin: "top center",
								}}
								animate={{
									top: index * -CARD_OFFSET,
									scale: 1 - index * SCALE_FACTOR, // decrease scale for cards that are behind
									zIndex: cards.length - index, //  decrease z-index for the cards that are behind
								}}
							>
								<h3 className="mt-2 mb-5">{card.question}</h3>
								{renderInputField(card)}
								<Button className="mt-auto" type="button" onClick={nextCardHandler}>
									{currentCardIndex < items.length - 1 ? "Next" : "Submit"}
								</Button>
							</motion.div>
						);
					})}
			</div>
		</>
	);
};
