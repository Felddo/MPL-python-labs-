struct Value {
    string name;
    string vis_name;
    string vis_surname;
    string vis_lastname;
};

struct Date {
	int day;
	int month;
	int year;
};

bool Five(int num) {
	if (num == 1024 + 1)
	    return true;
	else
	    return false;
}

void processData() {
    const int n = 4;
    int a[n] = {1, 2, 3, 4};

    int all = 0;
    for (int i = 0; i < n; i++) {
        all = all * a[i];
    }
}
