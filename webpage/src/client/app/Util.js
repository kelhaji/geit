export default class Util {
    static sum(values) {
        let sum = 0;

        values.forEach((value) => {
            sum += value;
        });

        return sum;
    }

    static cutEmail(email) {
        return email.split('@')[0];
    };

    static capitalize(s) {
      if (typeof s !== 'string') return '';
      return s.charAt(0).toUpperCase() + s.slice(1);
    };

    static formattedName(name) {
        return Util.capitalize(name.replace(/_/g, ' '));
    };
}