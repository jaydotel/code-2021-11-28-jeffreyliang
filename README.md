# Roll Up

Roll Up is a tool which can perform a quantity rollup calculation given part numbers and how they are grouped into assemblies.

It will:

1. Call BoM API to get the parts data
2. Group the data by parent
3. Perform the quantity rollup calculation while calling BoM API to get the `part_number` for each part
4. Output the `part_number` and total number of parts required to a .xlsx file

Naming in this application is similar to a tree data structure as each _part_ is treated similar to a node in a tree data structure where each part/node may have a parent part and children parts.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of `Python 3.8`, `pip` and `pipenv`.
* You have set up your operating system to run Python applications. The below set of instructions has only been tested on Linux and cannot be guaranteed it will work the same for Windows or Mac.
* An internet connection (required for making API calls to BoM)

## Installing Roll Up

To run Roll Up, follow these steps in your preferred terminal:

1. Clone the repository onto your local machine

`git clone https://github.com/jaydotel/qr-project-2021-11-28-jeffreyliang.git`

2. Navigate to the root directory and create a virtual environment and install required Python packages:

`pipenv install`

Alternatively, if you will be developing on this project:

`pipenv install --dev`

## Using Roll Up

To use Roll Up, follow these steps:

1. In the root folder, run Roll Up:

`python rollup.py <output_file_name>.xlsx`

If no output file name argument is provided, "output.xlsx" will be used.

2. A .xlsx file will be saved in the root directory.

## Running Unit Tests

From the project's root directory run:

`python -m unittest`
